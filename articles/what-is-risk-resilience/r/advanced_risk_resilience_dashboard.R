# Advanced risk and resilience dashboard workflow
#
# This workflow goes beyond a conceptual article by creating
# dashboard-ready outputs for:
# - hazard-exposure load
# - composite vulnerability
# - composite capacity
# - systemic risk
# - resilience capacity
# - justice-adjusted vulnerability
# - resilience gaps
# - intervention scenarios
# - regional and domain summaries

library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/what-is-risk-resilience"
data_file <- file.path(base_dir, "data", "risk_resilience_system_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

required_cols <- c(
  "system_id",
  "system_name",
  "domain",
  "region",
  "hazard_type",
  "hazard_intensity",
  "exposure_index",
  "social_vulnerability",
  "infrastructure_vulnerability",
  "ecological_vulnerability",
  "adaptive_capacity",
  "governance_capacity",
  "ecological_buffer_capacity",
  "redundancy_index",
  "early_warning_capacity",
  "transformation_capacity",
  "supply_chain_dependency",
  "critical_infrastructure_dependency",
  "social_inequality_index"
)

missing_cols <- setdiff(required_cols, names(systems))
if (length(missing_cols) > 0) {
  stop(paste("Missing required columns:", paste(missing_cols, collapse = ", ")))
}

classify_band <- function(value, low, high) {
  case_when(
    value < low ~ "lower",
    value < high ~ "moderate",
    TRUE ~ "elevated"
  )
}

score_systems <- function(df) {
  df %>%
    mutate(
      hazard_exposure_load = hazard_intensity * exposure_index,

      composite_vulnerability =
        0.42 * social_vulnerability +
        0.32 * infrastructure_vulnerability +
        0.26 * ecological_vulnerability,

      composite_capacity =
        0.24 * adaptive_capacity +
        0.22 * governance_capacity +
        0.22 * ecological_buffer_capacity +
        0.14 * redundancy_index +
        0.10 * early_warning_capacity +
        0.08 * transformation_capacity,

      base_risk =
        hazard_exposure_load *
        (1 + composite_vulnerability) *
        (1 - composite_capacity),

      cascade_multiplier =
        1 +
        0.24 * supply_chain_dependency +
        0.24 * critical_infrastructure_dependency +
        0.22 * social_inequality_index +
        0.16 * ecological_vulnerability +
        0.14 * infrastructure_vulnerability,

      systemic_risk_score = base_risk * cascade_multiplier,

      resilience_capacity_score =
        0.20 * adaptive_capacity +
        0.18 * governance_capacity +
        0.18 * ecological_buffer_capacity +
        0.14 * redundancy_index +
        0.12 * early_warning_capacity +
        0.18 * transformation_capacity,

      justice_adjusted_vulnerability =
        composite_vulnerability * (1 + 0.35 * social_inequality_index),

      resilience_gap = pmax(0, systemic_risk_score - resilience_capacity_score),

      transformation_readiness =
        0.35 * transformation_capacity +
        0.25 * governance_capacity +
        0.20 * adaptive_capacity +
        0.20 * redundancy_index,

      risk_band = classify_band(systemic_risk_score, 0.25, 0.55),
      resilience_band = classify_band(resilience_capacity_score, 0.40, 0.65),

      priority_class = case_when(
        risk_band == "elevated" & resilience_band != "elevated" ~
          "urgent_risk_reduction",
        justice_adjusted_vulnerability > 0.75 ~
          "justice_centered_adaptation",
        resilience_gap > 0.20 ~
          "capacity_building_priority",
        transformation_readiness > 0.65 ~
          "transformation_leverage",
        TRUE ~
          "monitor_and_maintain"
      )
    ) %>%
    arrange(desc(systemic_risk_score))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "preparedness_upgrade",
    "ecological_buffer_restoration",
    "justice_centered_adaptation",
    "deep_resilience_transformation"
  ),
  hazard_reduction = c(0.00, 0.02, 0.08, 0.04, 0.10),
  vulnerability_reduction = c(0.00, 0.05, 0.08, 0.18, 0.22),
  adaptive_capacity_gain = c(0.00, 0.10, 0.07, 0.14, 0.22),
  governance_capacity_gain = c(0.00, 0.08, 0.06, 0.14, 0.20),
  ecological_buffer_gain = c(0.00, 0.04, 0.24, 0.10, 0.22),
  redundancy_gain = c(0.00, 0.08, 0.06, 0.10, 0.18),
  early_warning_gain = c(0.00, 0.18, 0.06, 0.12, 0.18),
  transformation_gain = c(0.00, 0.05, 0.08, 0.16, 0.26)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    hazard_intensity = pmax(0, hazard_intensity * (1 - hazard_reduction)),

    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    infrastructure_vulnerability = pmax(0, infrastructure_vulnerability * (1 - vulnerability_reduction)),
    ecological_vulnerability = pmax(0, ecological_vulnerability * (1 - vulnerability_reduction)),

    adaptive_capacity = pmin(1, adaptive_capacity + adaptive_capacity_gain),
    governance_capacity = pmin(1, governance_capacity + governance_capacity_gain),
    ecological_buffer_capacity = pmin(1, ecological_buffer_capacity + ecological_buffer_gain),
    redundancy_index = pmin(1, redundancy_index + redundancy_gain),
    early_warning_capacity = pmin(1, early_warning_capacity + early_warning_gain),
    transformation_capacity = pmin(1, transformation_capacity + transformation_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_systemic_risk = mean(systemic_risk_score),
    mean_resilience_capacity = mean(resilience_capacity_score),
    mean_resilience_gap = mean(resilience_gap),
    elevated_risk_systems = sum(risk_band == "elevated"),
    urgent_systems = sum(priority_class == "urgent_risk_reduction"),
    justice_priority_systems = sum(priority_class == "justice_centered_adaptation"),
    .groups = "drop"
  ) %>%
  arrange(mean_systemic_risk)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_systemic_risk = mean(systemic_risk_score),
    mean_resilience_capacity = mean(resilience_capacity_score),
    mean_resilience_gap = mean(resilience_gap),
    mean_justice_adjusted_vulnerability = mean(justice_adjusted_vulnerability),
    mean_transformation_readiness = mean(transformation_readiness),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_systemic_risk))

regional_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_hazard_exposure_load = mean(hazard_exposure_load),
    mean_composite_vulnerability = mean(composite_vulnerability),
    mean_composite_capacity = mean(composite_capacity),
    mean_systemic_risk = mean(systemic_risk_score),
    mean_resilience_capacity = mean(resilience_capacity_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_systemic_risk))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    hazard_type,
    hazard_exposure_load,
    composite_vulnerability,
    composite_capacity,
    systemic_risk_score,
    resilience_capacity_score,
    justice_adjusted_vulnerability,
    resilience_gap,
    transformation_readiness
  ) %>%
  pivot_longer(
    cols = c(
      hazard_exposure_load,
      composite_vulnerability,
      composite_capacity,
      systemic_risk_score,
      resilience_capacity_score,
      justice_adjusted_vulnerability,
      resilience_gap,
      transformation_readiness
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_advanced_risk_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_advanced_risk_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_advanced_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_advanced_domain_summary.csv"))
write_csv(regional_summary, file.path(output_dir, "r_advanced_regional_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_advanced_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
