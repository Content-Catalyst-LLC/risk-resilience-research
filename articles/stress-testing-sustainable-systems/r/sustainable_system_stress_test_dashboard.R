library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/stress-testing-sustainable-systems"
data_file <- file.path(base_dir, "data", "sustainable_system_stress_test_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_stress_tests <- function(df) {
  df %>%
    mutate(
      stress_load =
        hazard_intensity *
        exposure *
        (1 + 0.35 * social_vulnerability) *
        (1 + 0.30 * interdependence_exposure),

      resilience_capacity =
        0.24 * baseline_capacity +
        0.20 * redundancy +
        0.20 * recovery_capacity +
        0.18 * governance_capacity +
        0.18 * monitoring_maturity,

      failure_pressure =
        stress_load *
        (1 - 0.45 * resilience_capacity),

      threshold_proximity =
        pmin(
          1.5,
          stress_load /
          (0.20 + threshold_level + resilience_capacity)
        ),

      service_continuity_gap =
        pmax(0, stress_load - resilience_capacity),

      stress_test_priority_score =
        service_continuity_gap +
        0.35 * threshold_proximity +
        0.25 * social_vulnerability +
        0.25 * interdependence_exposure,

      diagnostic_priority = case_when(
        threshold_proximity > 0.75 ~
          "reduce_threshold_proximity",
        service_continuity_gap > 0.35 ~
          "close_service_continuity_gap",
        redundancy < 0.40 ~
          "increase_redundancy_and_buffers",
        recovery_capacity < 0.40 ~
          "strengthen_recovery_capacity",
        governance_capacity < 0.40 ~
          "strengthen_governance_and_coordination",
        monitoring_maturity < 0.40 ~
          "improve_monitoring_and_early_warning",
        TRUE ~
          "monitor_and_retest_under_updated_scenarios"
      )
    ) %>%
    arrange(desc(stress_test_priority_score), desc(threshold_proximity))
}

scored <- score_stress_tests(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "moderate_compound_stress",
    "severe_compound_stress",
    "redundancy_and_recovery_investment",
    "governance_monitoring_and_early_warning",
    "integrated_resilience_upgrade"
  ),
  hazard_intensity_increase = c(0, .10, .22, .10, .10, .16),
  exposure_increase = c(0, .08, .18, .08, .08, .14),
  vulnerability_increase = c(0, .08, .16, .06, .06, .12),
  interdependence_increase = c(0, .08, .18, .08, .08, .14),
  redundancy_gain = c(0, 0, 0, .28, .12, .34),
  recovery_gain = c(0, 0, 0, .32, .18, .34),
  governance_gain = c(0, 0, 0, .14, .34, .34),
  monitoring_gain = c(0, 0, 0, .16, .34, .34),
  threshold_gain = c(0, 0, 0, .10, .12, .24)
)

scenario_scores <- list()

for (i in seq_len(nrow(scenario_parameters))) {
  p <- scenario_parameters[i, ]

  scenario_systems <- systems %>%
    mutate(
      hazard_intensity = pmin(1, hazard_intensity + p$hazard_intensity_increase),
      exposure = pmin(1, exposure + p$exposure_increase),
      social_vulnerability = pmin(1, social_vulnerability + p$vulnerability_increase),
      interdependence_exposure = pmin(1, interdependence_exposure + p$interdependence_increase),
      redundancy = pmin(1, redundancy + p$redundancy_gain),
      recovery_capacity = pmin(1, recovery_capacity + p$recovery_gain),
      governance_capacity = pmin(1, governance_capacity + p$governance_gain),
      monitoring_maturity = pmin(1, monitoring_maturity + p$monitoring_gain),
      threshold_level = pmin(1, threshold_level + p$threshold_gain)
    )

  scenario_scores[[i]] <- score_stress_tests(scenario_systems) %>%
    mutate(scenario = p$scenario)
}

scenario_scores <- bind_rows(scenario_scores)

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_stress_load = mean(stress_load),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_failure_pressure = mean(failure_pressure),
    mean_threshold_proximity = mean(threshold_proximity),
    mean_continuity_gap = mean(service_continuity_gap),
    mean_priority = mean(stress_test_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_priority))

sector_summary <- scored %>%
  group_by(sector) %>%
  summarise(
    systems = n(),
    mean_stress_load = mean(stress_load),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_failure_pressure = mean(failure_pressure),
    mean_threshold_proximity = mean(threshold_proximity),
    mean_continuity_gap = mean(service_continuity_gap),
    mean_priority = mean(stress_test_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_priority))

context_summary <- scored %>%
  group_by(stress_context) %>%
  summarise(
    systems = n(),
    mean_hazard_intensity = mean(hazard_intensity),
    mean_exposure = mean(exposure),
    mean_vulnerability = mean(social_vulnerability),
    mean_interdependence = mean(interdependence_exposure),
    mean_threshold_proximity = mean(threshold_proximity),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_threshold_proximity))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    sector,
    stress_context,
    stress_load,
    resilience_capacity,
    failure_pressure,
    threshold_proximity,
    service_continuity_gap,
    stress_test_priority_score
  ) %>%
  pivot_longer(
    cols = c(
      stress_load,
      resilience_capacity,
      failure_pressure,
      threshold_proximity,
      service_continuity_gap,
      stress_test_priority_score
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_sustainable_system_stress_test_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_sustainable_system_stress_test_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(sector_summary, file.path(output_dir, "r_sector_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(sector_summary)
print(context_summary)
