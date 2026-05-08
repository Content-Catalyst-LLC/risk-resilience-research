library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/cyber-risk-digital-dependency-and-system-resilience"
data_file <- file.path(base_dir, "data", "cyber_dependency_resilience_panel.csv")
dependency_file <- file.path(base_dir, "data", "digital_dependency_matrix.csv")
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
      cyber_disruption_pressure =
        digital_criticality *
        (
          0.18 * threat_pressure +
          0.16 * technical_vulnerability_exposure +
          0.15 * dependency_concentration +
          0.15 * identity_access_weakness +
          0.14 * vendor_supply_chain_exposure +
          0.12 * operational_technology_exposure +
          0.10 * data_integrity_risk
        ),

      cyber_resilience_capacity =
        0.20 * recovery_capacity +
        0.18 * governance_capacity +
        0.17 * backup_redundancy_capacity +
        0.16 * monitoring_maturity +
        0.14 * logging_maturity +
        0.15 * incident_exercise_maturity,

      systemic_cyber_risk =
        cyber_disruption_pressure *
        (1 + 0.35 * dependency_concentration) *
        (1 + 0.30 * user_vulnerability) *
        (1 - 0.45 * cyber_resilience_capacity)
    )

  cascading_dependency_exposure <- as.numeric(
    dependency_matrix %*% direct_scores$systemic_cyber_risk
  )

  direct_scores %>%
    mutate(
      cascading_dependency_exposure = cascading_dependency_exposure,

      service_continuity_gap =
        pmax(
          0,
          digital_criticality +
          systemic_cyber_risk +
          0.50 * cascading_dependency_exposure -
          cyber_resilience_capacity
        ),

      recovery_priority_score =
        service_continuity_gap +
        0.30 * digital_criticality +
        0.25 * user_vulnerability +
        0.25 * cascading_dependency_exposure,

      diagnostic_priority = case_when(
        identity_access_weakness > 0.65 ~
          "strengthen_identity_and_access_controls",
        vendor_supply_chain_exposure > 0.65 ~
          "reduce_vendor_and_software_supply_chain_exposure",
        backup_redundancy_capacity < 0.40 ~
          "improve_backups_redundancy_and_recovery",
        governance_capacity < 0.40 ~
          "strengthen_cyber_governance_and_accountability",
        cascading_dependency_exposure > 0.45 ~
          "map_and_reduce_cascading_digital_dependencies",
        service_continuity_gap > 0.85 ~
          "close_service_continuity_gap",
        TRUE ~
          "monitor_and_strengthen_systemic_cyber_resilience"
      )
    ) %>%
    arrange(desc(recovery_priority_score), desc(service_continuity_gap))
}

scored <- score_systems(systems, dependency_matrix)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "identity_and_access_resilience",
    "vendor_and_dependency_governance",
    "backup_recovery_and_continuity",
    "ot_and_data_integrity_protection",
    "integrated_systemic_cyber_resilience"
  ),
  threat_reduction = c(0, .08, .08, .06, .10, .30),
  vulnerability_reduction = c(0, .10, .12, .10, .16, .34),
  dependency_reduction = c(0, .10, .28, .10, .10, .30),
  identity_weakness_reduction = c(0, .34, .16, .12, .12, .34),
  vendor_exposure_reduction = c(0, .12, .34, .12, .12, .34),
  ot_exposure_reduction = c(0, .06, .08, .10, .34, .34),
  data_integrity_reduction = c(0, .10, .12, .12, .34, .34),
  recovery_gain = c(0, .14, .16, .34, .18, .34),
  governance_gain = c(0, .20, .28, .22, .22, .34),
  backup_gain = c(0, .18, .18, .34, .18, .34),
  monitoring_gain = c(0, .18, .18, .20, .24, .34),
  logging_gain = c(0, .18, .20, .22, .24, .34),
  exercise_gain = c(0, .18, .20, .30, .20, .34),
  user_vulnerability_reduction = c(0, .08, .10, .12, .10, .28),
  matrix_dependency_reduction = c(0, .10, .30, .12, .12, .34)
)

scenario_scores <- list()

for (i in seq_len(nrow(scenario_parameters))) {
  p <- scenario_parameters[i, ]

  scenario_systems <- systems %>%
    mutate(
      threat_pressure = pmax(0, threat_pressure * (1 - p$threat_reduction)),
      technical_vulnerability_exposure = pmax(0, technical_vulnerability_exposure * (1 - p$vulnerability_reduction)),
      dependency_concentration = pmax(0, dependency_concentration * (1 - p$dependency_reduction)),
      identity_access_weakness = pmax(0, identity_access_weakness * (1 - p$identity_weakness_reduction)),
      vendor_supply_chain_exposure = pmax(0, vendor_supply_chain_exposure * (1 - p$vendor_exposure_reduction)),
      operational_technology_exposure = pmax(0, operational_technology_exposure * (1 - p$ot_exposure_reduction)),
      data_integrity_risk = pmax(0, data_integrity_risk * (1 - p$data_integrity_reduction)),
      recovery_capacity = pmin(1, recovery_capacity + p$recovery_gain),
      governance_capacity = pmin(1, governance_capacity + p$governance_gain),
      backup_redundancy_capacity = pmin(1, backup_redundancy_capacity + p$backup_gain),
      monitoring_maturity = pmin(1, monitoring_maturity + p$monitoring_gain),
      logging_maturity = pmin(1, logging_maturity + p$logging_gain),
      incident_exercise_maturity = pmin(1, incident_exercise_maturity + p$exercise_gain),
      user_vulnerability = pmax(0, user_vulnerability * (1 - p$user_vulnerability_reduction))
    )

  scenario_dependency_matrix <- dependency_matrix * (1 - p$matrix_dependency_reduction)

  scenario_scores[[i]] <- score_systems(scenario_systems, scenario_dependency_matrix) %>%
    mutate(scenario = p$scenario)
}

scenario_scores <- bind_rows(scenario_scores)

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_disruption_pressure = mean(cyber_disruption_pressure),
    mean_resilience_capacity = mean(cyber_resilience_capacity),
    mean_systemic_risk = mean(systemic_cyber_risk),
    mean_cascading_exposure = mean(cascading_dependency_exposure),
    mean_continuity_gap = mean(service_continuity_gap),
    mean_recovery_priority = mean(recovery_priority_score),
    .groups = "drop"
  ) %>%
  arrange(mean_recovery_priority)

sector_summary <- scored %>%
  group_by(sector) %>%
  summarise(
    systems = n(),
    mean_disruption_pressure = mean(cyber_disruption_pressure),
    mean_resilience_capacity = mean(cyber_resilience_capacity),
    mean_systemic_risk = mean(systemic_cyber_risk),
    mean_cascading_exposure = mean(cascading_dependency_exposure),
    mean_continuity_gap = mean(service_continuity_gap),
    mean_recovery_priority = mean(recovery_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_recovery_priority))

context_summary <- scored %>%
  group_by(service_context) %>%
  summarise(
    systems = n(),
    mean_criticality = mean(digital_criticality),
    mean_identity_weakness = mean(identity_access_weakness),
    mean_vendor_exposure = mean(vendor_supply_chain_exposure),
    mean_resilience_capacity = mean(cyber_resilience_capacity),
    mean_continuity_gap = mean(service_continuity_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_continuity_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    sector,
    service_context,
    cyber_disruption_pressure,
    cyber_resilience_capacity,
    systemic_cyber_risk,
    cascading_dependency_exposure,
    service_continuity_gap,
    recovery_priority_score
  ) %>%
  pivot_longer(
    cols = c(
      cyber_disruption_pressure,
      cyber_resilience_capacity,
      systemic_cyber_risk,
      cascading_dependency_exposure,
      service_continuity_gap,
      recovery_priority_score
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_cyber_dependency_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_cyber_dependency_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(sector_summary, file.path(output_dir, "r_sector_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(sector_summary)
print(context_summary)
