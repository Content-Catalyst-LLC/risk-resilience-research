library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/ecosystem-resilience-and-natural-buffers"
data_file <- file.path(base_dir, "data", "ecosystem_buffer_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      natural_buffer_capacity =
        0.24 * ecosystem_condition +
        0.20 * ecological_connectivity +
        0.20 * functional_biodiversity +
        0.18 * maintenance_capacity +
        0.18 * restoration_investment,

      hazard_exposure_pressure =
        hazard_pressure *
        exposure *
        (1 + 0.35 * social_vulnerability),

      buffer_adjusted_risk =
        hazard_exposure_pressure *
        (1 - 0.45 * natural_buffer_capacity) *
        (1 - 0.25 * governance_capacity),

      ecological_fragility =
        0.28 * (1 - ecosystem_condition) +
        0.24 * (1 - ecological_connectivity) +
        0.22 * (1 - functional_biodiversity) +
        0.14 * (1 - maintenance_capacity) +
        0.12 * degradation_pressure,

      justice_weighted_ecosystem_risk =
        (buffer_adjusted_risk + ecological_fragility) *
        (1 + 0.30 * social_vulnerability),

      ecosystem_resilience_gap =
        pmax(0, justice_weighted_ecosystem_risk - natural_buffer_capacity),

      diagnostic_priority = case_when(
        ecosystem_condition < 0.40 ~
          "restore_ecosystem_condition",
        ecological_connectivity < 0.40 ~
          "reconnect_habitats_and_buffers",
        functional_biodiversity < 0.40 ~
          "protect_functional_biodiversity",
        hazard_pressure > 0.74 ~
          "reduce_exposure_to_hazard_pressure",
        governance_capacity < 0.42 ~
          "strengthen_ecological_governance",
        ecosystem_resilience_gap > 0.55 ~
          "close_ecosystem_resilience_gap",
        TRUE ~
          "monitor_and_preserve_natural_buffers"
      )
    ) %>%
    arrange(desc(ecosystem_resilience_gap), desc(justice_weighted_ecosystem_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "ecosystem_restoration",
    "connectivity_and_biodiversity",
    "governance_and_maintenance",
    "justice_centered_buffer_protection",
    "integrated_ecosystem_resilience"
  ),
  condition_gain = c(0, .22, .14, .12, .18, .30),
  connectivity_gain = c(0, .16, .30, .12, .18, .30),
  biodiversity_gain = c(0, .18, .30, .10, .16, .30),
  maintenance_gain = c(0, .16, .12, .30, .22, .30),
  restoration_gain = c(0, .30, .18, .20, .24, .34),
  hazard_reduction = c(0, .06, .04, .06, .10, .18),
  exposure_reduction = c(0, .06, .04, .08, .18, .22),
  vulnerability_reduction = c(0, .08, .06, .10, .28, .30),
  governance_gain = c(0, .12, .12, .30, .26, .30),
  degradation_reduction = c(0, .24, .18, .20, .24, .30)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    ecosystem_condition = pmin(1, ecosystem_condition + condition_gain),
    ecological_connectivity = pmin(1, ecological_connectivity + connectivity_gain),
    functional_biodiversity = pmin(1, functional_biodiversity + biodiversity_gain),
    maintenance_capacity = pmin(1, maintenance_capacity + maintenance_gain),
    restoration_investment = pmin(1, restoration_investment + restoration_gain),
    hazard_pressure = pmax(0, hazard_pressure * (1 - hazard_reduction)),
    exposure = pmax(0, exposure * (1 - exposure_reduction)),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    degradation_pressure = pmax(0, degradation_pressure * (1 - degradation_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_buffer_capacity = mean(natural_buffer_capacity),
    mean_buffer_adjusted_risk = mean(buffer_adjusted_risk),
    mean_ecological_fragility = mean(ecological_fragility),
    mean_justice_risk = mean(justice_weighted_ecosystem_risk),
    mean_resilience_gap = mean(ecosystem_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_buffer_capacity = mean(natural_buffer_capacity),
    mean_buffer_adjusted_risk = mean(buffer_adjusted_risk),
    mean_ecological_fragility = mean(ecological_fragility),
    mean_resilience_gap = mean(ecosystem_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

type_summary <- scored %>%
  group_by(ecosystem_type) %>%
  summarise(
    systems = n(),
    mean_ecosystem_condition = mean(ecosystem_condition),
    mean_connectivity = mean(ecological_connectivity),
    mean_biodiversity = mean(functional_biodiversity),
    mean_buffer_capacity = mean(natural_buffer_capacity),
    mean_resilience_gap = mean(ecosystem_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    ecosystem_type,
    natural_buffer_capacity,
    hazard_exposure_pressure,
    buffer_adjusted_risk,
    ecological_fragility,
    justice_weighted_ecosystem_risk,
    ecosystem_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      natural_buffer_capacity,
      hazard_exposure_pressure,
      buffer_adjusted_risk,
      ecological_fragility,
      justice_weighted_ecosystem_risk,
      ecosystem_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_ecosystem_buffer_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_ecosystem_buffer_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(type_summary, file.path(output_dir, "r_type_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(type_summary)
