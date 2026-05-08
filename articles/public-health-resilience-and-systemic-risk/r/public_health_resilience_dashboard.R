library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/public-health-resilience-and-systemic-risk"
data_file <- file.path(base_dir, "data", "public_health_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      public_health_threat_pressure =
        health_hazard_pressure *
        exposure *
        (1 + 0.40 * social_health_vulnerability),

      public_health_resilience_capacity =
        0.16 * surveillance_capacity +
        0.14 * prevention_capacity +
        0.16 * essential_service_continuity +
        0.14 * workforce_capacity +
        0.12 * supply_chain_reliability +
        0.12 * public_trust +
        0.08 * communication_capacity +
        0.08 * recovery_capacity,

      systemic_health_risk =
        public_health_threat_pressure *
        (1 - 0.45 * public_health_resilience_capacity) *
        (1 + 0.35 * inequality_pressure) *
        (1 + 0.15 * repeated_health_disruption_pressure),

      continuity_gap =
        pmax(0, essential_service_demand - essential_service_continuity),

      trust_adjusted_response_capacity =
        pmin(
          1.5,
          (
            0.34 * surveillance_capacity +
            0.33 * communication_capacity +
            0.33 * prevention_capacity
          ) *
          (1 + 0.30 * public_trust)
        ),

      public_health_resilience_gap =
        pmax(
          0,
          systemic_health_risk +
          continuity_gap -
          trust_adjusted_response_capacity
        ),

      diagnostic_priority = case_when(
        surveillance_capacity < 0.42 ~
          "strengthen_surveillance_and_laboratories",
        essential_service_continuity < 0.42 ~
          "protect_essential_service_continuity",
        workforce_capacity < 0.42 ~
          "rebuild_workforce_capacity",
        supply_chain_reliability < 0.42 ~
          "stabilize_health_supply_chains",
        public_trust < 0.42 ~
          "repair_trust_and_risk_communication",
        public_health_resilience_gap > 0.55 ~
          "close_public_health_resilience_gap",
        TRUE ~
          "monitor_and_strengthen_public_health_resilience"
      )
    ) %>%
    arrange(desc(public_health_resilience_gap), desc(systemic_health_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "surveillance_and_laboratory_strengthening",
    "essential_service_continuity",
    "workforce_and_supply_chain_resilience",
    "trust_communication_and_equity",
    "integrated_public_health_resilience"
  ),
  hazard_reduction = c(0, .06, .06, .04, .06, .18),
  exposure_reduction = c(0, .06, .08, .06, .10, .24),
  vulnerability_reduction = c(0, .08, .10, .08, .28, .30),
  surveillance_gain = c(0, .32, .14, .14, .16, .34),
  prevention_gain = c(0, .16, .18, .14, .20, .32),
  continuity_gain = c(0, .12, .34, .20, .16, .34),
  workforce_gain = c(0, .12, .22, .34, .16, .34),
  supply_chain_gain = c(0, .14, .20, .34, .12, .34),
  trust_gain = c(0, .10, .12, .10, .34, .34),
  communication_gain = c(0, .18, .14, .10, .34, .34),
  recovery_gain = c(0, .10, .26, .20, .18, .32),
  inequality_reduction = c(0, .08, .12, .10, .32, .34),
  service_demand_reduction = c(0, .08, .28, .18, .18, .32),
  repeated_disruption_reduction = c(0, .10, .18, .18, .18, .30)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    health_hazard_pressure = pmax(0, health_hazard_pressure * (1 - hazard_reduction)),
    exposure = pmax(0, exposure * (1 - exposure_reduction)),
    social_health_vulnerability = pmax(0, social_health_vulnerability * (1 - vulnerability_reduction)),
    surveillance_capacity = pmin(1, surveillance_capacity + surveillance_gain),
    prevention_capacity = pmin(1, prevention_capacity + prevention_gain),
    essential_service_continuity = pmin(1, essential_service_continuity + continuity_gain),
    workforce_capacity = pmin(1, workforce_capacity + workforce_gain),
    supply_chain_reliability = pmin(1, supply_chain_reliability + supply_chain_gain),
    public_trust = pmin(1, public_trust + trust_gain),
    communication_capacity = pmin(1, communication_capacity + communication_gain),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    inequality_pressure = pmax(0, inequality_pressure * (1 - inequality_reduction)),
    essential_service_demand = pmax(0, essential_service_demand * (1 - service_demand_reduction)),
    repeated_health_disruption_pressure = pmax(0, repeated_health_disruption_pressure * (1 - repeated_disruption_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_threat_pressure = mean(public_health_threat_pressure),
    mean_resilience_capacity = mean(public_health_resilience_capacity),
    mean_systemic_health_risk = mean(systemic_health_risk),
    mean_continuity_gap = mean(continuity_gap),
    mean_resilience_gap = mean(public_health_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_threat_pressure = mean(public_health_threat_pressure),
    mean_resilience_capacity = mean(public_health_resilience_capacity),
    mean_systemic_health_risk = mean(systemic_health_risk),
    mean_continuity_gap = mean(continuity_gap),
    mean_resilience_gap = mean(public_health_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

context_summary <- scored %>%
  group_by(health_risk_context) %>%
  summarise(
    systems = n(),
    mean_hazard_pressure = mean(health_hazard_pressure),
    mean_vulnerability = mean(social_health_vulnerability),
    mean_resilience_capacity = mean(public_health_resilience_capacity),
    mean_systemic_health_risk = mean(systemic_health_risk),
    mean_resilience_gap = mean(public_health_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    health_risk_context,
    public_health_threat_pressure,
    public_health_resilience_capacity,
    systemic_health_risk,
    continuity_gap,
    trust_adjusted_response_capacity,
    public_health_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      public_health_threat_pressure,
      public_health_resilience_capacity,
      systemic_health_risk,
      continuity_gap,
      trust_adjusted_response_capacity,
      public_health_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_public_health_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_public_health_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(context_summary)
