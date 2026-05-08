library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/migration-displacement-and-resilience"
data_file <- file.path(base_dir, "data", "migration_displacement_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

places <- read_csv(data_file, show_col_types = FALSE)

score_places <- function(df) {
  df %>%
    mutate(
      mobility_pressure =
        0.22 * hazard_pressure +
        0.20 * livelihood_stress +
        0.20 * conflict_insecurity_pressure +
        0.18 * exposure +
        0.20 * social_vulnerability,

      adaptive_mobility_capacity =
        0.16 * adaptive_capacity +
        0.15 * mobility_resources +
        0.16 * protection_access +
        0.14 * migration_network_strength +
        0.14 * destination_service_capacity +
        0.13 * host_community_support +
        0.12 * recovery_capacity,

      forced_displacement_risk =
        mobility_pressure *
        (1 + 0.35 * social_vulnerability) *
        (1 - 0.45 * adaptive_mobility_capacity),

      trapped_population_risk =
        pmax(
          0,
          mobility_pressure -
          mobility_resources -
          protection_access -
          migration_network_strength
        ),

      destination_stress =
        pmin(
          1.5,
          arrival_pressure /
          (
            0.35 +
            destination_service_capacity +
            host_community_support +
            recovery_capacity
          )
        ),

      mobility_resilience_gap =
        pmax(
          0,
          forced_displacement_risk +
          trapped_population_risk +
          destination_stress -
          adaptive_mobility_capacity
        ),

      diagnostic_priority = case_when(
        protection_access < 0.42 ~
          "strengthen_rights_and_protection_access",
        mobility_resources < 0.42 ~
          "expand_safe_mobility_resources",
        destination_service_capacity < 0.42 ~
          "invest_in_destination_services",
        host_community_support < 0.42 ~
          "support_host_communities",
        trapped_population_risk > 0.25 ~
          "protect_trapped_populations",
        mobility_resilience_gap > 0.55 ~
          "close_mobility_resilience_gap",
        TRUE ~
          "monitor_and_strengthen_adaptive_mobility"
      )
    ) %>%
    arrange(desc(mobility_resilience_gap), desc(forced_displacement_risk))
}

scored <- score_places(places)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "safe_mobility_and_protection",
    "origin_resilience_and_livelihoods",
    "host_community_service_investment",
    "trapped_population_protection",
    "integrated_mobility_resilience"
  ),
  hazard_reduction = c(0, .06, .18, .04, .10, .24),
  livelihood_stress_reduction = c(0, .08, .32, .06, .14, .34),
  conflict_reduction = c(0, .08, .10, .06, .08, .24),
  exposure_reduction = c(0, .08, .18, .06, .12, .28),
  vulnerability_reduction = c(0, .10, .22, .08, .28, .34),
  adaptive_capacity_gain = c(0, .14, .26, .14, .20, .34),
  mobility_resources_gain = c(0, .34, .18, .14, .30, .34),
  protection_access_gain = c(0, .34, .18, .16, .28, .34),
  network_gain = c(0, .18, .16, .14, .24, .32),
  destination_capacity_gain = c(0, .14, .12, .34, .18, .34),
  host_support_gain = c(0, .16, .14, .34, .18, .34),
  recovery_gain = c(0, .18, .18, .28, .20, .34),
  arrival_pressure_reduction = c(0, .08, .06, .22, .08, .28)
)

scenario_scores <- places %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    hazard_pressure = pmax(0, hazard_pressure * (1 - hazard_reduction)),
    livelihood_stress = pmax(0, livelihood_stress * (1 - livelihood_stress_reduction)),
    conflict_insecurity_pressure = pmax(0, conflict_insecurity_pressure * (1 - conflict_reduction)),
    exposure = pmax(0, exposure * (1 - exposure_reduction)),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    adaptive_capacity = pmin(1, adaptive_capacity + adaptive_capacity_gain),
    mobility_resources = pmin(1, mobility_resources + mobility_resources_gain),
    protection_access = pmin(1, protection_access + protection_access_gain),
    migration_network_strength = pmin(1, migration_network_strength + network_gain),
    destination_service_capacity = pmin(1, destination_service_capacity + destination_capacity_gain),
    host_community_support = pmin(1, host_community_support + host_support_gain),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    arrival_pressure = pmax(0, arrival_pressure * (1 - arrival_pressure_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_places(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_mobility_pressure = mean(mobility_pressure),
    mean_adaptive_capacity = mean(adaptive_mobility_capacity),
    mean_forced_displacement_risk = mean(forced_displacement_risk),
    mean_trapped_population_risk = mean(trapped_population_risk),
    mean_destination_stress = mean(destination_stress),
    mean_resilience_gap = mean(mobility_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    places = n(),
    mean_mobility_pressure = mean(mobility_pressure),
    mean_adaptive_capacity = mean(adaptive_mobility_capacity),
    mean_forced_displacement_risk = mean(forced_displacement_risk),
    mean_trapped_population_risk = mean(trapped_population_risk),
    mean_destination_stress = mean(destination_stress),
    mean_resilience_gap = mean(mobility_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

context_summary <- scored %>%
  group_by(mobility_context) %>%
  summarise(
    places = n(),
    mean_hazard_pressure = mean(hazard_pressure),
    mean_livelihood_stress = mean(livelihood_stress),
    mean_conflict_pressure = mean(conflict_insecurity_pressure),
    mean_adaptive_capacity = mean(adaptive_mobility_capacity),
    mean_resilience_gap = mean(mobility_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    place_id,
    place_name,
    region,
    mobility_context,
    mobility_pressure,
    adaptive_mobility_capacity,
    forced_displacement_risk,
    trapped_population_risk,
    destination_stress,
    mobility_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      mobility_pressure,
      adaptive_mobility_capacity,
      forced_displacement_risk,
      trapped_population_risk,
      destination_stress,
      mobility_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_migration_displacement_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_migration_displacement_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(context_summary)
