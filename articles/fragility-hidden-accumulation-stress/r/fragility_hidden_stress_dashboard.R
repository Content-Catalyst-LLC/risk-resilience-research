library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/fragility-hidden-accumulation-stress"
data_file <- file.path(base_dir, "data", "fragility_hidden_stress_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

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
      hidden_stress_index =
        0.20 * stress_accumulation +
        0.16 * buffer_erosion +
        0.14 * deferred_maintenance +
        0.13 * adaptation_debt +
        0.12 * ecological_support_erosion +
        0.13 * social_strain +
        0.12 * trust_erosion,

      drift_index =
        0.34 * institutional_drift +
        0.30 * signal_normalization +
        0.22 * standard_erosion +
        0.14 * (1 - monitoring_capacity),

      latent_instability =
        0.38 * threshold_proximity +
        0.26 * hidden_stress_index +
        0.20 * drift_index +
        0.16 * system_criticality,

      resilience_margin =
        0.34 * (1 - buffer_erosion) +
        0.24 * monitoring_capacity +
        0.24 * response_capacity +
        0.18 * (1 - threshold_proximity),

      performance_misalignment =
        pmax(0, visible_performance - (1 - hidden_stress_index)),

      fragility_score =
        (
          0.32 * hidden_stress_index +
          0.24 * drift_index +
          0.24 * latent_instability +
          0.20 * performance_misalignment
        ) *
        (1 + 0.25 * system_criticality),

      justice_weighted_fragility =
        fragility_score * (1 + 0.35 * justice_pressure),

      resilience_gap =
        pmax(0, justice_weighted_fragility - resilience_margin),

      fragility_band = classify_band(justice_weighted_fragility, 0.35, 0.70),
      margin_band = classify_band(resilience_margin, 0.40, 0.65),

      diagnostic_priority = case_when(
        threshold_proximity > 0.75 ~
          "threshold_avoidance_priority",
        drift_index > 0.65 ~
          "anti_drift_governance_priority",
        hidden_stress_index > 0.70 ~
          "hidden_stress_relief_priority",
        justice_pressure > 0.70 ~
          "justice_centered_margin_repair",
        performance_misalignment > 0.25 ~
          "performance_metric_redesign",
        TRUE ~
          "monitor_and_rebuild_margin"
      )
    ) %>%
    arrange(desc(resilience_gap), desc(justice_weighted_fragility), desc(latent_instability))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "monitoring_and_signal_repair",
    "maintenance_and_buffer_restoration",
    "anti_drift_governance",
    "justice_centered_stress_relief",
    "resilience_margin_rebuild"
  ),
  stress_reduction = c(0.00, 0.08, 0.08, 0.10, 0.16, 0.20),
  buffer_restoration = c(0.00, 0.08, 0.24, 0.14, 0.14, 0.26),
  maintenance_reduction = c(0.00, 0.08, 0.24, 0.16, 0.14, 0.26),
  drift_reduction = c(0.00, 0.14, 0.08, 0.24, 0.16, 0.24),
  signal_denormalization = c(0.00, 0.24, 0.10, 0.22, 0.18, 0.24),
  standards_restoration = c(0.00, 0.14, 0.12, 0.24, 0.16, 0.24),
  threshold_reduction = c(0.00, 0.06, 0.10, 0.12, 0.12, 0.20),
  adaptation_debt_reduction = c(0.00, 0.10, 0.10, 0.20, 0.18, 0.24),
  ecological_restoration = c(0.00, 0.04, 0.14, 0.12, 0.16, 0.24),
  social_strain_reduction = c(0.00, 0.08, 0.08, 0.14, 0.24, 0.24),
  trust_repair = c(0.00, 0.12, 0.08, 0.18, 0.24, 0.24),
  monitoring_gain = c(0.00, 0.24, 0.10, 0.20, 0.18, 0.24),
  response_gain = c(0.00, 0.12, 0.16, 0.22, 0.22, 0.26)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    stress_accumulation = pmax(0, stress_accumulation * (1 - stress_reduction)),
    buffer_erosion = pmax(0, buffer_erosion * (1 - buffer_restoration)),
    deferred_maintenance = pmax(0, deferred_maintenance * (1 - maintenance_reduction)),
    institutional_drift = pmax(0, institutional_drift * (1 - drift_reduction)),
    signal_normalization = pmax(0, signal_normalization * (1 - signal_denormalization)),
    standard_erosion = pmax(0, standard_erosion * (1 - standards_restoration)),
    threshold_proximity = pmax(0, threshold_proximity * (1 - threshold_reduction)),
    adaptation_debt = pmax(0, adaptation_debt * (1 - adaptation_debt_reduction)),
    ecological_support_erosion = pmax(0, ecological_support_erosion * (1 - ecological_restoration)),
    social_strain = pmax(0, social_strain * (1 - social_strain_reduction)),
    trust_erosion = pmax(0, trust_erosion * (1 - trust_repair)),
    monitoring_capacity = pmin(1, monitoring_capacity + monitoring_gain),
    response_capacity = pmin(1, response_capacity + response_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_hidden_stress = mean(hidden_stress_index),
    mean_drift = mean(drift_index),
    mean_latent_instability = mean(latent_instability),
    mean_resilience_margin = mean(resilience_margin),
    mean_fragility = mean(justice_weighted_fragility),
    mean_resilience_gap = mean(resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_visible_performance = mean(visible_performance),
    mean_hidden_stress = mean(hidden_stress_index),
    mean_drift = mean(drift_index),
    mean_latent_instability = mean(latent_instability),
    mean_resilience_margin = mean(resilience_margin),
    mean_fragility = mean(justice_weighted_fragility),
    mean_resilience_gap = mean(resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    stress_type,
    visible_performance,
    hidden_stress_index,
    drift_index,
    latent_instability,
    resilience_margin,
    justice_weighted_fragility,
    resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      visible_performance,
      hidden_stress_index,
      drift_index,
      latent_instability,
      resilience_margin,
      justice_weighted_fragility,
      resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_fragility_hidden_stress_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_fragility_hidden_stress_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
