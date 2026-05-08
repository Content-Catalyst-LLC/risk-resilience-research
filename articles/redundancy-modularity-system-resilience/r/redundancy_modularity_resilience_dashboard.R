library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/redundancy-modularity-system-resilience"
data_file <- file.path(base_dir, "data", "redundancy_modularity_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      redundancy_index =
        0.32 * redundancy_capacity +
        0.24 * backup_diversity +
        0.22 * pathway_diversity +
        0.22 * spare_capacity,

      modularity_index =
        0.42 * modularity_capacity +
        0.28 * containment_strength +
        0.18 * (1 - coupling_intensity) +
        0.12 * (1 - dependency_concentration),

      resilience_design_capacity =
        0.30 * redundancy_index +
        0.30 * modularity_index +
        0.16 * restoration_capacity +
        0.14 * monitoring_capacity +
        0.10 * governance_coordination,

      propagation_pressure =
        primary_failure_pressure *
        (1 + coupling_intensity) *
        (1 + dependency_concentration) *
        (1 + 0.25 * system_criticality) *
        (1 - 0.45 * modularity_index),

      continuity_capacity =
        0.28 * redundancy_index +
        0.22 * restoration_capacity +
        0.20 * governance_coordination +
        0.16 * monitoring_capacity +
        0.14 * containment_strength,

      efficiency_fragility_pressure =
        0.34 * efficiency_pressure +
        0.22 * (1 - redundancy_capacity) +
        0.22 * (1 - modularity_capacity) +
        0.22 * dependency_concentration,

      justice_weighted_resilience_gap =
        pmax(
          0,
          (
            0.34 * propagation_pressure +
            0.28 * efficiency_fragility_pressure +
            0.22 * social_vulnerability +
            0.16 * system_criticality
          ) *
          (1 + 0.30 * social_vulnerability) -
          continuity_capacity
        ),

      diagnostic_priority = case_when(
        redundancy_index < 0.42 ~
          "redundancy_rebuild_priority",
        modularity_index < 0.42 ~
          "modularity_and_containment_priority",
        propagation_pressure > 1.40 ~
          "propagation_reduction_priority",
        continuity_capacity < 0.45 ~
          "essential_function_continuity_gap",
        efficiency_fragility_pressure > 0.72 ~
          "deoptimization_for_resilience",
        social_vulnerability > 0.72 ~
          "justice_centered_resilience_design",
        TRUE ~
          "monitor_and_preserve_resilience_design"
      )
    ) %>%
    arrange(desc(justice_weighted_resilience_gap), desc(propagation_pressure), desc(efficiency_fragility_pressure))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "redundancy_rebuild",
    "modularity_and_containment",
    "continuity_and_restoration",
    "justice_centered_resilience_design",
    "resilience_design_portfolio"
  ),
  failure_pressure_reduction = c(0.00, 0.06, 0.06, 0.08, 0.10, 0.18),
  redundancy_gain = c(0.00, 0.28, 0.10, 0.18, 0.20, 0.30),
  modularity_gain = c(0.00, 0.10, 0.30, 0.18, 0.20, 0.30),
  backup_diversity_gain = c(0.00, 0.24, 0.10, 0.16, 0.18, 0.28),
  pathway_diversity_gain = c(0.00, 0.22, 0.16, 0.18, 0.20, 0.28),
  spare_capacity_gain = c(0.00, 0.24, 0.12, 0.18, 0.20, 0.28),
  coupling_reduction = c(0.00, 0.08, 0.22, 0.12, 0.14, 0.26),
  dependency_reduction = c(0.00, 0.10, 0.20, 0.12, 0.14, 0.26),
  containment_gain = c(0.00, 0.10, 0.30, 0.18, 0.20, 0.30),
  restoration_gain = c(0.00, 0.12, 0.12, 0.28, 0.20, 0.30),
  monitoring_gain = c(0.00, 0.10, 0.12, 0.18, 0.20, 0.28),
  governance_gain = c(0.00, 0.10, 0.16, 0.24, 0.24, 0.28),
  vulnerability_reduction = c(0.00, 0.08, 0.08, 0.12, 0.26, 0.24),
  efficiency_pressure_reduction = c(0.00, 0.12, 0.10, 0.12, 0.16, 0.24)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    primary_failure_pressure = pmax(0, primary_failure_pressure * (1 - failure_pressure_reduction)),
    redundancy_capacity = pmin(1, redundancy_capacity + redundancy_gain),
    modularity_capacity = pmin(1, modularity_capacity + modularity_gain),
    backup_diversity = pmin(1, backup_diversity + backup_diversity_gain),
    pathway_diversity = pmin(1, pathway_diversity + pathway_diversity_gain),
    spare_capacity = pmin(1, spare_capacity + spare_capacity_gain),
    coupling_intensity = pmax(0, coupling_intensity * (1 - coupling_reduction)),
    dependency_concentration = pmax(0, dependency_concentration * (1 - dependency_reduction)),
    containment_strength = pmin(1, containment_strength + containment_gain),
    restoration_capacity = pmin(1, restoration_capacity + restoration_gain),
    monitoring_capacity = pmin(1, monitoring_capacity + monitoring_gain),
    governance_coordination = pmin(1, governance_coordination + governance_gain),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    efficiency_pressure = pmax(0, efficiency_pressure * (1 - efficiency_pressure_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_redundancy = mean(redundancy_index),
    mean_modularity = mean(modularity_index),
    mean_design_capacity = mean(resilience_design_capacity),
    mean_propagation_pressure = mean(propagation_pressure),
    mean_continuity_capacity = mean(continuity_capacity),
    mean_efficiency_fragility = mean(efficiency_fragility_pressure),
    mean_resilience_gap = mean(justice_weighted_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_redundancy = mean(redundancy_index),
    mean_modularity = mean(modularity_index),
    mean_design_capacity = mean(resilience_design_capacity),
    mean_propagation_pressure = mean(propagation_pressure),
    mean_continuity_capacity = mean(continuity_capacity),
    mean_efficiency_fragility = mean(efficiency_fragility_pressure),
    mean_resilience_gap = mean(justice_weighted_resilience_gap),
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
    redundancy_index,
    modularity_index,
    resilience_design_capacity,
    propagation_pressure,
    continuity_capacity,
    efficiency_fragility_pressure,
    justice_weighted_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      redundancy_index,
      modularity_index,
      resilience_design_capacity,
      propagation_pressure,
      continuity_capacity,
      efficiency_fragility_pressure,
      justice_weighted_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_redundancy_modularity_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_redundancy_modularity_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
