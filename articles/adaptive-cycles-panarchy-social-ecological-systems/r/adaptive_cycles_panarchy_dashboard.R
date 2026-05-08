library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/adaptive-cycles-panarchy-social-ecological-systems"
data_file <- file.path(base_dir, "data", "adaptive_cycles_panarchy_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      conservation_rigidity_index =
        0.34 * connectedness +
        0.34 * rigidity +
        0.18 * cross_scale_dependency +
        0.14 * (1 - governance_flexibility),

      release_risk_index =
        0.34 * release_pressure +
        0.24 * conservation_rigidity_index +
        0.18 * revolt_pressure +
        0.14 * system_criticality +
        0.10 * inequality_pressure,

      reorganization_potential_index =
        0.28 * reorganization_capacity +
        0.22 * novelty_potential +
        0.18 * memory_capacity +
        0.16 * institutional_learning +
        0.16 * governance_flexibility,

      remember_capacity =
        0.34 * memory_capacity +
        0.24 * institutional_learning +
        0.22 * ecological_buffer_condition +
        0.20 * governance_flexibility,

      revolt_cascade_pressure =
        revolt_pressure *
        (1 + cross_scale_dependency) *
        (1 + 0.35 * system_criticality) *
        (1 - 0.35 * remember_capacity),

      resilience_trap_index =
        0.32 * conservation_rigidity_index +
        0.24 * (1 - reorganization_capacity) +
        0.18 * (1 - novelty_potential) +
        0.16 * inequality_pressure +
        0.10 * system_criticality,

      transformation_readiness =
        0.28 * reorganization_potential_index +
        0.24 * resilience_capacity +
        0.18 * institutional_learning +
        0.16 * ecological_buffer_condition +
        0.14 * governance_flexibility,

      justice_weighted_reorganization_gap =
        pmax(
          0,
          (
            0.32 * release_risk_index +
            0.26 * revolt_cascade_pressure +
            0.22 * resilience_trap_index +
            0.20 * inequality_pressure
          ) *
          (1 + 0.30 * inequality_pressure) -
          transformation_readiness
        ),

      diagnostic_priority = case_when(
        conservation_rigidity_index > 0.72 ~
          "anti_rigidity_transition",
        release_risk_index > 0.75 ~
          "release_pressure_management",
        reorganization_potential_index < 0.45 ~
          "reorganization_capacity_building",
        revolt_cascade_pressure > 0.80 ~
          "cross_scale_revolt_containment",
        resilience_trap_index > 0.70 ~
          "resilience_trap_escape",
        inequality_pressure > 0.70 ~
          "justice_centered_reorganization",
        TRUE ~
          "monitor_and_preserve_adaptive_capacity"
      )
    ) %>%
    arrange(desc(justice_weighted_reorganization_gap), desc(release_risk_index), desc(resilience_trap_index))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "memory_and_learning",
    "reorganization_capacity",
    "anti_rigidity_transition",
    "justice_centered_reorganization",
    "panarchy_resilience_portfolio"
  ),
  rigidity_reduction = c(0.00, 0.08, 0.12, 0.24, 0.18, 0.28),
  connectedness_rebalancing = c(0.00, 0.04, 0.08, 0.18, 0.12, 0.22),
  resilience_gain = c(0.00, 0.12, 0.18, 0.20, 0.22, 0.30),
  release_pressure_reduction = c(0.00, 0.06, 0.10, 0.18, 0.14, 0.24),
  reorganization_gain = c(0.00, 0.14, 0.28, 0.22, 0.26, 0.30),
  novelty_gain = c(0.00, 0.10, 0.24, 0.18, 0.24, 0.28),
  memory_gain = c(0.00, 0.24, 0.16, 0.16, 0.20, 0.28),
  revolt_reduction = c(0.00, 0.06, 0.08, 0.14, 0.18, 0.24),
  dependency_reduction = c(0.00, 0.06, 0.08, 0.14, 0.16, 0.24),
  inequality_reduction = c(0.00, 0.08, 0.10, 0.14, 0.28, 0.26),
  learning_gain = c(0.00, 0.28, 0.20, 0.22, 0.24, 0.30),
  ecological_buffer_gain = c(0.00, 0.12, 0.18, 0.20, 0.22, 0.30),
  governance_flexibility_gain = c(0.00, 0.14, 0.22, 0.26, 0.26, 0.30)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    rigidity = pmax(0, rigidity * (1 - rigidity_reduction)),
    connectedness = pmax(0, connectedness * (1 - connectedness_rebalancing)),
    resilience_capacity = pmin(1, resilience_capacity + resilience_gain),
    release_pressure = pmax(0, release_pressure * (1 - release_pressure_reduction)),
    reorganization_capacity = pmin(1, reorganization_capacity + reorganization_gain),
    novelty_potential = pmin(1, novelty_potential + novelty_gain),
    memory_capacity = pmin(1, memory_capacity + memory_gain),
    revolt_pressure = pmax(0, revolt_pressure * (1 - revolt_reduction)),
    cross_scale_dependency = pmax(0, cross_scale_dependency * (1 - dependency_reduction)),
    inequality_pressure = pmax(0, inequality_pressure * (1 - inequality_reduction)),
    institutional_learning = pmin(1, institutional_learning + learning_gain),
    ecological_buffer_condition = pmin(1, ecological_buffer_condition + ecological_buffer_gain),
    governance_flexibility = pmin(1, governance_flexibility + governance_flexibility_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_rigidity = mean(conservation_rigidity_index),
    mean_release_risk = mean(release_risk_index),
    mean_reorganization = mean(reorganization_potential_index),
    mean_remember_capacity = mean(remember_capacity),
    mean_revolt_pressure = mean(revolt_cascade_pressure),
    mean_trap = mean(resilience_trap_index),
    mean_transformation = mean(transformation_readiness),
    mean_reorganization_gap = mean(justice_weighted_reorganization_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_reorganization_gap)

scale_summary <- scored %>%
  group_by(scale_level) %>%
  summarise(
    systems = n(),
    mean_rigidity = mean(conservation_rigidity_index),
    mean_release_risk = mean(release_risk_index),
    mean_reorganization = mean(reorganization_potential_index),
    mean_remember_capacity = mean(remember_capacity),
    mean_revolt_pressure = mean(revolt_cascade_pressure),
    mean_trap = mean(resilience_trap_index),
    mean_transformation = mean(transformation_readiness),
    mean_reorganization_gap = mean(justice_weighted_reorganization_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_reorganization_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    scale_level,
    domain,
    region,
    adaptive_phase,
    conservation_rigidity_index,
    release_risk_index,
    reorganization_potential_index,
    remember_capacity,
    revolt_cascade_pressure,
    resilience_trap_index,
    transformation_readiness,
    justice_weighted_reorganization_gap
  ) %>%
  pivot_longer(
    cols = c(
      conservation_rigidity_index,
      release_risk_index,
      reorganization_potential_index,
      remember_capacity,
      revolt_cascade_pressure,
      resilience_trap_index,
      transformation_readiness,
      justice_weighted_reorganization_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_adaptive_cycles_panarchy_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_adaptive_cycles_panarchy_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(scale_summary, file.path(output_dir, "r_scale_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(scale_summary)
