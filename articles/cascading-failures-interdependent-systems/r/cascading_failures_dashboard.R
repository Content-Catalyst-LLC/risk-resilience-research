library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/cascading-failures-interdependent-systems"
data_file <- file.path(base_dir, "data", "cascading_failures_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      dependency_pressure =
        0.34 * dependency_density +
        0.30 * hidden_coupling +
        0.22 * critical_node_exposure +
        0.14 * system_criticality,

      containment_capacity =
        0.22 * backup_capacity +
        0.24 * modularity_capacity +
        0.20 * redundancy_capacity +
        0.18 * monitoring_capacity +
        0.16 * cross_sector_coordination,

      governance_response_capacity =
        0.30 * cross_sector_coordination +
        0.24 * restoration_speed +
        0.20 * governance_readiness +
        0.14 * monitoring_capacity +
        0.12 * public_trust,

      propagation_likelihood =
        initiating_shock_severity *
        (1 + dependency_pressure) *
        (1 + 0.35 * cascade_exposure) *
        (1 - 0.45 * containment_capacity),

      cascade_amplification =
        propagation_likelihood *
        (1 + system_criticality) *
        (1 + social_vulnerability) *
        (1 - 0.35 * governance_response_capacity),

      essential_function_continuity =
        0.26 * backup_capacity +
        0.22 * redundancy_capacity +
        0.20 * restoration_speed +
        0.18 * cross_sector_coordination +
        0.14 * public_trust,

      continuity_gap =
        pmax(0, cascade_amplification - essential_function_continuity),

      justice_weighted_cascade_risk =
        (
          0.34 * propagation_likelihood +
          0.30 * cascade_amplification +
          0.20 * continuity_gap +
          0.16 * social_vulnerability
        ) *
        (1 + 0.30 * social_vulnerability),

      diagnostic_priority = case_when(
        dependency_pressure > 0.78 ~
          "dependency_mapping_priority",
        critical_node_exposure > 0.78 ~
          "critical_node_hardening",
        containment_capacity < 0.42 ~
          "modularity_and_redundancy_rebuild",
        governance_response_capacity < 0.45 ~
          "cross_sector_governance_priority",
        continuity_gap > 0.45 ~
          "essential_function_continuity_gap",
        social_vulnerability > 0.72 ~
          "justice_centered_containment",
        TRUE ~
          "monitor_and_strengthen_containment"
      )
    ) %>%
    arrange(desc(justice_weighted_cascade_risk), desc(continuity_gap), desc(cascade_amplification))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "dependency_mapping_and_monitoring",
    "modularity_and_redundancy",
    "critical_node_hardening",
    "cross_sector_continuity",
    "justice_centered_containment",
    "systemic_resilience_portfolio"
  ),
  shock_reduction = c(0.00, 0.04, 0.06, 0.10, 0.08, 0.10, 0.18),
  dependency_reduction = c(0.00, 0.06, 0.12, 0.10, 0.10, 0.12, 0.24),
  coupling_reduction = c(0.00, 0.10, 0.12, 0.12, 0.10, 0.12, 0.24),
  critical_node_reduction = c(0.00, 0.08, 0.12, 0.26, 0.12, 0.14, 0.26),
  backup_gain = c(0.00, 0.06, 0.22, 0.20, 0.18, 0.20, 0.30),
  modularity_gain = c(0.00, 0.06, 0.26, 0.18, 0.18, 0.20, 0.30),
  coordination_gain = c(0.00, 0.14, 0.12, 0.14, 0.28, 0.24, 0.30),
  restoration_gain = c(0.00, 0.08, 0.12, 0.18, 0.26, 0.22, 0.30),
  redundancy_gain = c(0.00, 0.06, 0.26, 0.18, 0.18, 0.20, 0.30),
  vulnerability_reduction = c(0.00, 0.06, 0.08, 0.10, 0.12, 0.26, 0.24),
  governance_gain = c(0.00, 0.12, 0.12, 0.16, 0.24, 0.24, 0.30),
  cascade_exposure_reduction = c(0.00, 0.08, 0.14, 0.16, 0.18, 0.20, 0.28),
  monitoring_gain = c(0.00, 0.26, 0.10, 0.14, 0.20, 0.20, 0.28),
  trust_gain = c(0.00, 0.10, 0.08, 0.12, 0.18, 0.24, 0.26)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    initiating_shock_severity = pmax(0, initiating_shock_severity * (1 - shock_reduction)),
    dependency_density = pmax(0, dependency_density * (1 - dependency_reduction)),
    hidden_coupling = pmax(0, hidden_coupling * (1 - coupling_reduction)),
    critical_node_exposure = pmax(0, critical_node_exposure * (1 - critical_node_reduction)),
    backup_capacity = pmin(1, backup_capacity + backup_gain),
    modularity_capacity = pmin(1, modularity_capacity + modularity_gain),
    cross_sector_coordination = pmin(1, cross_sector_coordination + coordination_gain),
    restoration_speed = pmin(1, restoration_speed + restoration_gain),
    redundancy_capacity = pmin(1, redundancy_capacity + redundancy_gain),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    governance_readiness = pmin(1, governance_readiness + governance_gain),
    cascade_exposure = pmax(0, cascade_exposure * (1 - cascade_exposure_reduction)),
    monitoring_capacity = pmin(1, monitoring_capacity + monitoring_gain),
    public_trust = pmin(1, public_trust + trust_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_dependency_pressure = mean(dependency_pressure),
    mean_containment_capacity = mean(containment_capacity),
    mean_governance_response = mean(governance_response_capacity),
    mean_propagation = mean(propagation_likelihood),
    mean_cascade_amplification = mean(cascade_amplification),
    mean_continuity = mean(essential_function_continuity),
    mean_continuity_gap = mean(continuity_gap),
    mean_cascade_risk = mean(justice_weighted_cascade_risk),
    .groups = "drop"
  ) %>%
  arrange(mean_cascade_risk)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_dependency_pressure = mean(dependency_pressure),
    mean_containment_capacity = mean(containment_capacity),
    mean_governance_response = mean(governance_response_capacity),
    mean_propagation = mean(propagation_likelihood),
    mean_cascade_amplification = mean(cascade_amplification),
    mean_continuity = mean(essential_function_continuity),
    mean_continuity_gap = mean(continuity_gap),
    mean_cascade_risk = mean(justice_weighted_cascade_risk),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_cascade_risk))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    stress_type,
    dependency_pressure,
    containment_capacity,
    governance_response_capacity,
    propagation_likelihood,
    cascade_amplification,
    essential_function_continuity,
    continuity_gap,
    justice_weighted_cascade_risk
  ) %>%
  pivot_longer(
    cols = c(
      dependency_pressure,
      containment_capacity,
      governance_response_capacity,
      propagation_likelihood,
      cascade_amplification,
      essential_function_continuity,
      continuity_gap,
      justice_weighted_cascade_risk
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_cascading_failures_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_cascading_failures_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
