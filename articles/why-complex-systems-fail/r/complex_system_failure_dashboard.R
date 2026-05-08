library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/why-complex-systems-fail"
data_file <- file.path(base_dir, "data", "complex_system_failure_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

classify_band <- function(value, low, high) {
  case_when(
    value < low ~ "lower",
    value < high ~ "moderate",
    TRUE ~ "elevated"
  )
}

score_systems <- function(df) {
  df %>%
    mutate(
      coupling_pressure =
        0.48 * dependency_density +
        0.36 * hidden_coupling +
        0.16 * system_criticality,

      deterioration_pressure =
        0.30 * feedback_delay +
        0.28 * (1 - signal_visibility) +
        0.22 * maintenance_deficit +
        0.20 * adaptation_debt,

      slack_deficit =
        0.34 * (1 - buffer_capacity) +
        0.30 * (1 - redundancy_capacity) +
        0.20 * (1 - modularity_capacity) +
        0.16 * optimization_pressure,

      resilience_capacity =
        0.20 * buffer_capacity +
        0.20 * redundancy_capacity +
        0.18 * modularity_capacity +
        0.18 * monitoring_capacity +
        0.14 * governance_coordination +
        0.10 * signal_visibility,

      cascade_potential =
        coupling_pressure *
        (1 + external_stress) *
        (1 + 0.5 * system_criticality) *
        (1 - 0.35 * modularity_capacity),

      structural_fragility =
        0.30 * coupling_pressure +
        0.28 * deterioration_pressure +
        0.24 * slack_deficit +
        0.18 * social_vulnerability,

      failure_risk =
        structural_fragility *
        (1 + external_stress) *
        (1 + 0.35 * system_criticality) *
        (1 - 0.45 * resilience_capacity),

      failure_gap =
        pmax(0, failure_risk - resilience_capacity),

      signal_gap =
        pmax(0, deterioration_pressure - monitoring_capacity),

      resilience_priority_score =
        pmin(
          1,
          0.35 * failure_gap +
            0.25 * pmin(1, cascade_potential) +
            0.20 * signal_gap +
            0.20 * social_vulnerability
        ),

      failure_risk_band = classify_band(failure_risk, 0.35, 0.70),
      cascade_band = classify_band(cascade_potential, 0.65, 1.20),

      diagnostic_priority = case_when(
        cascade_potential > 1.20 ~
          "cascade_containment_priority",
        signal_gap > 0.25 ~
          "monitoring_and_feedback_priority",
        slack_deficit > 0.60 ~
          "restore_slack_and_redundancy",
        adaptation_debt > 0.65 ~
          "adaptation_debt_reduction",
        TRUE ~
          "monitor_and_strengthen_resilience"
      )
    ) %>%
    arrange(desc(resilience_priority_score), desc(failure_gap), desc(cascade_potential))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "monitoring_and_signal_upgrade",
    "redundancy_and_modularity",
    "deoptimization_for_resilience",
    "adaptive_governance",
    "system_resilience_portfolio"
  ),
  dependency_reduction = c(0.00, 0.02, 0.10, 0.08, 0.06, 0.14),
  coupling_reduction = c(0.00, 0.02, 0.12, 0.08, 0.08, 0.16),
  delay_reduction = c(0.00, 0.10, 0.04, 0.04, 0.12, 0.16),
  signal_visibility_gain = c(0.00, 0.24, 0.08, 0.08, 0.16, 0.22),
  buffer_gain = c(0.00, 0.06, 0.18, 0.20, 0.12, 0.24),
  redundancy_gain = c(0.00, 0.04, 0.24, 0.18, 0.12, 0.24),
  modularity_gain = c(0.00, 0.04, 0.24, 0.16, 0.14, 0.24),
  adaptation_debt_reduction = c(0.00, 0.08, 0.06, 0.12, 0.18, 0.20),
  optimization_pressure_reduction = c(0.00, 0.04, 0.08, 0.24, 0.12, 0.22),
  maintenance_gain = c(0.00, 0.08, 0.10, 0.16, 0.16, 0.22),
  monitoring_gain = c(0.00, 0.24, 0.08, 0.10, 0.18, 0.24),
  governance_gain = c(0.00, 0.10, 0.12, 0.10, 0.24, 0.24)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    dependency_density = pmax(0, dependency_density * (1 - dependency_reduction)),
    hidden_coupling = pmax(0, hidden_coupling * (1 - coupling_reduction)),
    feedback_delay = pmax(0, feedback_delay * (1 - delay_reduction)),
    signal_visibility = pmin(1, signal_visibility + signal_visibility_gain),
    buffer_capacity = pmin(1, buffer_capacity + buffer_gain),
    redundancy_capacity = pmin(1, redundancy_capacity + redundancy_gain),
    modularity_capacity = pmin(1, modularity_capacity + modularity_gain),
    adaptation_debt = pmax(0, adaptation_debt * (1 - adaptation_debt_reduction)),
    optimization_pressure = pmax(0, optimization_pressure * (1 - optimization_pressure_reduction)),
    maintenance_deficit = pmax(0, maintenance_deficit * (1 - maintenance_gain)),
    monitoring_capacity = pmin(1, monitoring_capacity + monitoring_gain),
    governance_coordination = pmin(1, governance_coordination + governance_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_coupling_pressure = mean(coupling_pressure),
    mean_deterioration_pressure = mean(deterioration_pressure),
    mean_slack_deficit = mean(slack_deficit),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_cascade_potential = mean(cascade_potential),
    mean_failure_risk = mean(failure_risk),
    mean_failure_gap = mean(failure_gap),
    mean_priority_score = mean(resilience_priority_score),
    .groups = "drop"
  ) %>%
  arrange(mean_priority_score)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_coupling_pressure = mean(coupling_pressure),
    mean_deterioration_pressure = mean(deterioration_pressure),
    mean_slack_deficit = mean(slack_deficit),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_cascade_potential = mean(cascade_potential),
    mean_failure_risk = mean(failure_risk),
    mean_failure_gap = mean(failure_gap),
    mean_priority_score = mean(resilience_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_priority_score))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    stress_type,
    coupling_pressure,
    deterioration_pressure,
    slack_deficit,
    resilience_capacity,
    cascade_potential,
    failure_risk,
    failure_gap,
    resilience_priority_score
  ) %>%
  pivot_longer(
    cols = c(
      coupling_pressure,
      deterioration_pressure,
      slack_deficit,
      resilience_capacity,
      cascade_potential,
      failure_risk,
      failure_gap,
      resilience_priority_score
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_complex_system_failure_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_complex_system_failure_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
