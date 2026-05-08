library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/thresholds-tipping-points-system-breakdown"
data_file <- file.path(base_dir, "data", "threshold_tipping_system_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      effective_margin =
        0.42 * resilience_margin +
        0.24 * buffer_capacity +
        0.18 * monitoring_capacity +
        0.16 * governance_readiness,

      threshold_pressure =
        0.34 * stress_load +
        0.22 * stress_rate +
        0.26 * threshold_proximity +
        0.18 * feedback_destabilization,

      tipping_pressure =
        threshold_pressure *
        (1 + 0.35 * feedback_destabilization) *
        (1 + 0.25 * stress_rate) *
        (1 - 0.45 * effective_margin),

      regime_shift_likelihood =
        pmin(
          1.5,
          0.34 * tipping_pressure +
            0.26 * threshold_proximity +
            0.20 * feedback_destabilization +
            0.20 * (1 - regime_shift_reversibility)
        ),

      cascade_potential =
        regime_shift_likelihood *
        (1 + interdependency_density) *
        (1 + 0.5 * cascade_exposure) *
        (1 + 0.35 * system_criticality),

      recovery_difficulty =
        pmin(
          1.5,
          0.32 * regime_shift_likelihood +
            0.24 * (1 - recovery_capacity) +
            0.22 * (1 - regime_shift_reversibility) +
            0.22 * social_vulnerability
        ),

      breakdown_risk =
        0.34 * regime_shift_likelihood +
        0.28 * pmin(1.5, cascade_potential) +
        0.20 * recovery_difficulty +
        0.18 * social_vulnerability,

      justice_weighted_breakdown_risk =
        breakdown_risk * (1 + 0.35 * justice_pressure),

      resilience_gap =
        pmax(0, justice_weighted_breakdown_risk - effective_margin),

      diagnostic_priority = case_when(
        threshold_proximity > 0.80 ~
          "critical_threshold_avoidance",
        cascade_potential > 1.40 ~
          "cascade_containment_priority",
        regime_shift_likelihood > 0.75 ~
          "regime_shift_prevention",
        effective_margin < 0.45 ~
          "resilience_margin_rebuild",
        justice_pressure > 0.70 ~
          "justice_centered_breakdown_prevention",
        TRUE ~
          "monitor_and_preserve_margin"
      )
    ) %>%
    arrange(desc(resilience_gap), desc(justice_weighted_breakdown_risk), desc(cascade_potential))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "early_warning_and_monitoring",
    "margin_and_buffer_restoration",
    "cascade_containment",
    "justice_centered_threshold_avoidance",
    "resilience_before_breakdown"
  ),
  stress_reduction = c(0.00, 0.04, 0.08, 0.06, 0.10, 0.18),
  stress_rate_reduction = c(0.00, 0.06, 0.08, 0.06, 0.10, 0.16),
  margin_gain = c(0.00, 0.08, 0.26, 0.14, 0.18, 0.30),
  buffer_gain = c(0.00, 0.06, 0.28, 0.16, 0.20, 0.30),
  monitoring_gain = c(0.00, 0.26, 0.10, 0.14, 0.18, 0.26),
  feedback_stabilization = c(0.00, 0.12, 0.14, 0.18, 0.18, 0.26),
  threshold_retreat = c(0.00, 0.08, 0.16, 0.12, 0.18, 0.24),
  interdependency_reduction = c(0.00, 0.04, 0.06, 0.20, 0.12, 0.22),
  cascade_reduction = c(0.00, 0.06, 0.08, 0.28, 0.14, 0.26),
  governance_gain = c(0.00, 0.16, 0.12, 0.18, 0.22, 0.26),
  recovery_gain = c(0.00, 0.08, 0.18, 0.16, 0.20, 0.26),
  vulnerability_reduction = c(0.00, 0.06, 0.08, 0.10, 0.24, 0.22),
  justice_reduction = c(0.00, 0.06, 0.08, 0.10, 0.24, 0.22),
  reversibility_gain = c(0.00, 0.08, 0.14, 0.12, 0.18, 0.24)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    stress_load = pmax(0, stress_load * (1 - stress_reduction)),
    stress_rate = pmax(0, stress_rate * (1 - stress_rate_reduction)),
    resilience_margin = pmin(1, resilience_margin + margin_gain),
    buffer_capacity = pmin(1, buffer_capacity + buffer_gain),
    monitoring_capacity = pmin(1, monitoring_capacity + monitoring_gain),
    feedback_destabilization = pmax(0, feedback_destabilization * (1 - feedback_stabilization)),
    threshold_proximity = pmax(0, threshold_proximity * (1 - threshold_retreat)),
    interdependency_density = pmax(0, interdependency_density * (1 - interdependency_reduction)),
    cascade_exposure = pmax(0, cascade_exposure * (1 - cascade_reduction)),
    governance_readiness = pmin(1, governance_readiness + governance_gain),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    justice_pressure = pmax(0, justice_pressure * (1 - justice_reduction)),
    regime_shift_reversibility = pmin(1, regime_shift_reversibility + reversibility_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_effective_margin = mean(effective_margin),
    mean_threshold_pressure = mean(threshold_pressure),
    mean_tipping_pressure = mean(tipping_pressure),
    mean_regime_shift_likelihood = mean(regime_shift_likelihood),
    mean_cascade_potential = mean(cascade_potential),
    mean_recovery_difficulty = mean(recovery_difficulty),
    mean_breakdown_risk = mean(justice_weighted_breakdown_risk),
    mean_resilience_gap = mean(resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_effective_margin = mean(effective_margin),
    mean_threshold_pressure = mean(threshold_pressure),
    mean_tipping_pressure = mean(tipping_pressure),
    mean_regime_shift_likelihood = mean(regime_shift_likelihood),
    mean_cascade_potential = mean(cascade_potential),
    mean_recovery_difficulty = mean(recovery_difficulty),
    mean_breakdown_risk = mean(justice_weighted_breakdown_risk),
    mean_resilience_gap = mean(resilience_gap),
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
    effective_margin,
    threshold_pressure,
    tipping_pressure,
    regime_shift_likelihood,
    cascade_potential,
    recovery_difficulty,
    justice_weighted_breakdown_risk,
    resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      effective_margin,
      threshold_pressure,
      tipping_pressure,
      regime_shift_likelihood,
      cascade_potential,
      recovery_difficulty,
      justice_weighted_breakdown_risk,
      resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_threshold_tipping_system_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_threshold_tipping_system_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
