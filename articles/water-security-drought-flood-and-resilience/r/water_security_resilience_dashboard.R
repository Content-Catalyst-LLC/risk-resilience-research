library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/water-security-drought-flood-and-resilience"
data_file <- file.path(base_dir, "data", "water_security_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      water_stress_ratio =
        pmin(2, water_demand_pressure / (water_availability + 0.05)),

      water_security_capacity =
        0.20 * water_availability +
        0.18 * infrastructure_reliability +
        0.16 * water_quality +
        0.18 * ecosystem_buffer_condition +
        0.16 * governance_capacity +
        0.12 * social_protection_capacity,

      hydrological_risk_pressure =
        0.24 * drought_pressure +
        0.24 * flood_exposure +
        0.18 * pmin(1, water_stress_ratio) +
        0.18 * pollution_pressure +
        0.16 * maintenance_deficit,

      systemic_water_vulnerability =
        0.24 * livelihood_water_dependency +
        0.20 * (1 - recovery_capacity) +
        0.20 * critical_service_dependence +
        0.18 * (1 - governance_capacity) +
        0.18 * inequality_pressure,

      justice_weighted_water_risk =
        (hydrological_risk_pressure + systemic_water_vulnerability) *
        (1 + 0.30 * inequality_pressure),

      water_resilience_gap =
        pmax(0, justice_weighted_water_risk - water_security_capacity),

      diagnostic_priority = case_when(
        drought_pressure > 0.72 ~
          "drought_resilience_and_demand_management",
        flood_exposure > 0.72 ~
          "flood_risk_reduction_and_protection",
        water_quality < 0.42 ~
          "water_quality_and_public_health",
        ecosystem_buffer_condition < 0.40 ~
          "restore_ecological_water_buffers",
        governance_capacity < 0.42 ~
          "strengthen_water_governance",
        water_resilience_gap > 0.55 ~
          "close_water_resilience_gap",
        TRUE ~
          "monitor_and_preserve_water_security"
      )
    ) %>%
    arrange(desc(water_resilience_gap), desc(justice_weighted_water_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "drought_demand_management",
    "flood_and_ecosystem_buffers",
    "water_quality_and_public_health",
    "justice_centered_water_security",
    "integrated_water_resilience"
  ),
  drought_reduction = c(0, .18, .06, .04, .16, .24),
  flood_reduction = c(0, .02, .22, .08, .16, .24),
  demand_reduction = c(0, .20, .06, .08, .18, .26),
  availability_gain = c(0, .10, .08, .08, .18, .24),
  infrastructure_gain = c(0, .08, .14, .16, .22, .30),
  quality_gain = c(0, .06, .12, .30, .22, .30),
  ecosystem_gain = c(0, .10, .30, .14, .20, .30),
  governance_gain = c(0, .14, .14, .18, .26, .30),
  social_protection_gain = c(0, .10, .10, .18, .30, .30),
  livelihood_dependency_reduction = c(0, .10, .06, .08, .22, .26),
  critical_service_dependency_reduction = c(0, .06, .08, .10, .20, .26),
  inequality_reduction = c(0, .08, .08, .14, .30, .28),
  recovery_gain = c(0, .10, .12, .16, .28, .30),
  maintenance_reduction = c(0, .10, .14, .18, .24, .30),
  pollution_reduction = c(0, .08, .12, .28, .22, .30)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    drought_pressure = pmax(0, drought_pressure * (1 - drought_reduction)),
    flood_exposure = pmax(0, flood_exposure * (1 - flood_reduction)),
    water_demand_pressure = pmax(0, water_demand_pressure * (1 - demand_reduction)),
    water_availability = pmin(1, water_availability + availability_gain),
    infrastructure_reliability = pmin(1, infrastructure_reliability + infrastructure_gain),
    water_quality = pmin(1, water_quality + quality_gain),
    ecosystem_buffer_condition = pmin(1, ecosystem_buffer_condition + ecosystem_gain),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    social_protection_capacity = pmin(1, social_protection_capacity + social_protection_gain),
    livelihood_water_dependency = pmax(0, livelihood_water_dependency * (1 - livelihood_dependency_reduction)),
    critical_service_dependence = pmax(0, critical_service_dependence * (1 - critical_service_dependency_reduction)),
    inequality_pressure = pmax(0, inequality_pressure * (1 - inequality_reduction)),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    maintenance_deficit = pmax(0, maintenance_deficit * (1 - maintenance_reduction)),
    pollution_pressure = pmax(0, pollution_pressure * (1 - pollution_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_water_security_capacity = mean(water_security_capacity),
    mean_hydrological_risk = mean(hydrological_risk_pressure),
    mean_water_vulnerability = mean(systemic_water_vulnerability),
    mean_justice_weighted_risk = mean(justice_weighted_water_risk),
    mean_resilience_gap = mean(water_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_water_security_capacity = mean(water_security_capacity),
    mean_hydrological_risk = mean(hydrological_risk_pressure),
    mean_water_vulnerability = mean(systemic_water_vulnerability),
    mean_justice_weighted_risk = mean(justice_weighted_water_risk),
    mean_resilience_gap = mean(water_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

stress_summary <- scored %>%
  group_by(water_stress_type) %>%
  summarise(
    systems = n(),
    mean_drought_pressure = mean(drought_pressure),
    mean_flood_exposure = mean(flood_exposure),
    mean_water_security_capacity = mean(water_security_capacity),
    mean_hydrological_risk = mean(hydrological_risk_pressure),
    mean_resilience_gap = mean(water_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    water_stress_type,
    water_stress_ratio,
    water_security_capacity,
    hydrological_risk_pressure,
    systemic_water_vulnerability,
    justice_weighted_water_risk,
    water_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      water_stress_ratio,
      water_security_capacity,
      hydrological_risk_pressure,
      systemic_water_vulnerability,
      justice_weighted_water_risk,
      water_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_water_security_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_water_security_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(stress_summary, file.path(output_dir, "r_stress_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(stress_summary)
