library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/compound-climate-events-cascading-social-risk"
data_file <- file.path(base_dir, "data", "compound_climate_social_risk_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      compound_event_severity =
        0.42 * concurrent_hazard_intensity +
        0.34 * sequential_hazard_pressure +
        0.24 * exposure,

      social_sensitivity_index =
        0.30 * social_vulnerability +
        0.22 * health_system_strain +
        0.20 * food_water_energy_stress +
        0.16 * recovery_deficit +
        0.12 * inequality_pressure,

      system_fragility_index =
        0.30 * infrastructure_fragility +
        0.28 * cross_sector_dependency +
        0.18 * food_water_energy_stress +
        0.14 * recovery_deficit +
        0.10 * (1 - communication_reliability),

      resilience_capacity =
        0.24 * governance_readiness +
        0.22 * ecological_buffer_condition +
        0.22 * social_protection_capacity +
        0.18 * communication_reliability +
        0.14 * (1 - recovery_deficit),

      cascade_potential =
        compound_event_severity *
        (1 + 0.45 * system_fragility_index) *
        (1 + 0.35 * cross_sector_dependency) *
        (1 - 0.30 * resilience_capacity),

      justice_weighted_social_risk =
        (
          0.38 * cascade_potential +
          0.30 * social_sensitivity_index +
          0.18 * recovery_deficit +
          0.14 * inequality_pressure
        ) *
        (1 + 0.35 * inequality_pressure),

      continuity_capacity =
        0.28 * governance_readiness +
        0.22 * social_protection_capacity +
        0.20 * communication_reliability +
        0.18 * ecological_buffer_condition +
        0.12 * (1 - infrastructure_fragility),

      compound_resilience_gap =
        pmax(0, justice_weighted_social_risk - continuity_capacity),

      diagnostic_priority = case_when(
        compound_event_severity > 0.76 ~
          "multi_hazard_preparedness",
        cross_sector_dependency > 0.76 ~
          "cross_sector_dependency_mapping",
        social_sensitivity_index > 0.72 ~
          "public_health_and_social_protection",
        governance_readiness < 0.45 ~
          "governance_and_warning_capacity",
        ecological_buffer_condition < 0.40 ~
          "restore_ecological_buffers",
        compound_resilience_gap > 0.22 ~
          "close_compound_resilience_gap",
        TRUE ~
          "monitor_and_strengthen_compound_resilience"
      )
    ) %>%
    arrange(desc(compound_resilience_gap), desc(justice_weighted_social_risk))
}

scored <- score_systems(systems)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_compound_event_severity = mean(compound_event_severity),
    mean_cascade_potential = mean(cascade_potential),
    mean_social_risk = mean(justice_weighted_social_risk),
    mean_continuity_capacity = mean(continuity_capacity),
    mean_resilience_gap = mean(compound_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

event_summary <- scored %>%
  group_by(event_type) %>%
  summarise(
    systems = n(),
    mean_compound_event_severity = mean(compound_event_severity),
    mean_system_fragility = mean(system_fragility_index),
    mean_cascade_potential = mean(cascade_potential),
    mean_resilience_gap = mean(compound_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    event_type,
    compound_event_severity,
    social_sensitivity_index,
    system_fragility_index,
    cascade_potential,
    justice_weighted_social_risk,
    continuity_capacity,
    compound_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      compound_event_severity,
      social_sensitivity_index,
      system_fragility_index,
      cascade_potential,
      justice_weighted_social_risk,
      continuity_capacity,
      compound_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_compound_climate_social_risk_scores.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(event_summary, file.path(output_dir, "r_event_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(region_summary)
print(event_summary)
