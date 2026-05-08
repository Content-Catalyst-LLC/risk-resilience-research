library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/critical-infrastructure-resilience-and-interdependent-systems"
data_file <- file.path(base_dir, "data", "critical_infrastructure_resilience_panel.csv")
dependency_file <- file.path(base_dir, "data", "infrastructure_dependency_matrix.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)
dependencies <- read_csv(dependency_file, show_col_types = FALSE)

dependency_matrix <- dependencies %>%
  select(-system_id) %>%
  as.matrix()

score_systems <- function(df, dependency_matrix) {
  direct_scores <- df %>%
    mutate(
      failure_pressure =
        criticality *
        hazard_exposure *
        asset_fragility *
        (1 + 0.35 * cyber_physical_risk)
    )

  interdependence_exposure <- as.numeric(
    dependency_matrix %*% direct_scores$failure_pressure
  )

  direct_scores %>%
    mutate(
      interdependence_exposure = interdependence_exposure,

      resilience_capacity =
        0.22 * redundancy +
        0.20 * maintenance_capacity +
        0.18 * governance_capacity +
        0.18 * recovery_capacity +
        0.12 * backup_capacity +
        0.10 * workforce_readiness,

      cascading_infrastructure_risk =
        (failure_pressure + interdependence_exposure) *
        (1 + 0.30 * social_vulnerability) *
        (1 - 0.45 * resilience_capacity),

      service_continuity_gap =
        pmax(0, service_demand_under_stress - resilience_capacity),

      recovery_priority_score =
        cascading_infrastructure_risk +
        0.35 * service_continuity_gap +
        0.25 * criticality +
        0.20 * social_vulnerability,

      diagnostic_priority = case_when(
        interdependence_exposure > 0.55 ~
          "map_dependencies_and_reduce_cascading_exposure",
        cyber_physical_risk > 0.65 ~
          "strengthen_cyber_physical_resilience",
        maintenance_capacity < 0.42 ~
          "restore_maintenance_and_asset_management",
        redundancy < 0.42 ~
          "build_redundancy_and_backup_capacity",
        governance_capacity < 0.42 ~
          "strengthen_governance_and_accountability",
        service_continuity_gap > 0.35 ~
          "close_service_continuity_gap",
        TRUE ~
          "monitor_and_strengthen_infrastructure_resilience"
      )
    ) %>%
    arrange(desc(recovery_priority_score), desc(cascading_infrastructure_risk))
}

scored <- score_systems(systems, dependency_matrix)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "dependency_mapping_and_redundancy",
    "maintenance_and_asset_management",
    "cyber_physical_resilience",
    "continuity_and_recovery_capacity",
    "integrated_infrastructure_resilience"
  ),
  hazard_reduction = c(0, .04, .06, .04, .06, .22),
  asset_fragility_reduction = c(0, .08, .30, .08, .12, .34),
  cyber_risk_reduction = c(0, .08, .08, .34, .12, .34),
  redundancy_gain = c(0, .34, .14, .18, .22, .34),
  maintenance_gain = c(0, .16, .34, .16, .20, .34),
  governance_gain = c(0, .22, .20, .30, .24, .34),
  recovery_gain = c(0, .18, .20, .22, .34, .34),
  backup_gain = c(0, .32, .18, .20, .30, .34),
  workforce_gain = c(0, .14, .20, .28, .30, .34),
  service_demand_reduction = c(0, .08, .08, .06, .24, .28),
  social_vulnerability_reduction = c(0, .08, .10, .08, .12, .30),
  dependency_reduction = c(0, .22, .08, .12, .14, .30)
)

scenario_scores <- purrr::map_dfr(seq_len(nrow(scenario_parameters)), function(i) {
  params <- scenario_parameters[i, ]

  scenario_systems <- systems %>%
    mutate(
      hazard_exposure = pmax(0, hazard_exposure * (1 - params$hazard_reduction)),
      asset_fragility = pmax(0, asset_fragility * (1 - params$asset_fragility_reduction)),
      cyber_physical_risk = pmax(0, cyber_physical_risk * (1 - params$cyber_risk_reduction)),
      redundancy = pmin(1, redundancy + params$redundancy_gain),
      maintenance_capacity = pmin(1, maintenance_capacity + params$maintenance_gain),
      governance_capacity = pmin(1, governance_capacity + params$governance_gain),
      recovery_capacity = pmin(1, recovery_capacity + params$recovery_gain),
      backup_capacity = pmin(1, backup_capacity + params$backup_gain),
      workforce_readiness = pmin(1, workforce_readiness + params$workforce_gain),
      service_demand_under_stress = pmax(0, service_demand_under_stress * (1 - params$service_demand_reduction)),
      social_vulnerability = pmax(0, social_vulnerability * (1 - params$social_vulnerability_reduction))
    )

  scenario_dependency_matrix <- dependency_matrix * (1 - params$dependency_reduction)

  score_systems(scenario_systems, scenario_dependency_matrix) %>%
    mutate(scenario = params$scenario)
})

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_failure_pressure = mean(failure_pressure),
    mean_interdependence_exposure = mean(interdependence_exposure),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_cascading_risk = mean(cascading_infrastructure_risk),
    mean_service_gap = mean(service_continuity_gap),
    mean_recovery_priority = mean(recovery_priority_score),
    .groups = "drop"
  ) %>%
  arrange(mean_recovery_priority)

sector_summary <- scored %>%
  group_by(sector) %>%
  summarise(
    systems = n(),
    mean_failure_pressure = mean(failure_pressure),
    mean_interdependence_exposure = mean(interdependence_exposure),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_cascading_risk = mean(cascading_infrastructure_risk),
    mean_service_gap = mean(service_continuity_gap),
    mean_recovery_priority = mean(recovery_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_recovery_priority))

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_failure_pressure = mean(failure_pressure),
    mean_interdependence_exposure = mean(interdependence_exposure),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_cascading_risk = mean(cascading_infrastructure_risk),
    mean_service_gap = mean(service_continuity_gap),
    mean_recovery_priority = mean(recovery_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_recovery_priority))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    sector,
    region,
    failure_pressure,
    interdependence_exposure,
    resilience_capacity,
    cascading_infrastructure_risk,
    service_continuity_gap,
    recovery_priority_score
  ) %>%
  pivot_longer(
    cols = c(
      failure_pressure,
      interdependence_exposure,
      resilience_capacity,
      cascading_infrastructure_risk,
      service_continuity_gap,
      recovery_priority_score
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_critical_infrastructure_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_critical_infrastructure_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(sector_summary, file.path(output_dir, "r_sector_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(sector_summary)
print(region_summary)
