library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/risk-uncertainty-complexity"
data_file <- file.path(base_dir, "data", "risk_uncertainty_complexity_panel.csv")
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
      expected_risk = hazard_probability * expected_loss_index,
      combined_uncertainty = (probability_uncertainty + loss_uncertainty) / 2,
      uncertainty_adjusted_risk = expected_risk * (1 + combined_uncertainty),
      complexity_multiplier =
        1 +
        0.28 * dependency_density +
        0.24 * feedback_strength +
        0.24 * threshold_sensitivity +
        0.24 * adaptive_behavior,
      systemic_risk = uncertainty_adjusted_risk * complexity_multiplier,
      robust_response_capacity =
        0.22 * monitoring_capacity +
        0.20 * redundancy_capacity +
        0.18 * flexibility_capacity +
        0.20 * institutional_learning +
        0.20 * adaptive_governance_capacity,
      vulnerability_weighted_systemic_risk =
        systemic_risk *
        (1 + 0.30 * social_vulnerability) *
        (1 + 0.20 * criticality_index),
      resilience_gap =
        pmax(0, vulnerability_weighted_systemic_risk - robust_response_capacity),
      risk_band = classify_band(vulnerability_weighted_systemic_risk, 0.25, 0.55),
      capacity_band = classify_band(robust_response_capacity, 0.40, 0.65),
      priority_class = case_when(
        risk_band == "elevated" & capacity_band != "elevated" ~
          "urgent_systemic_risk_reduction",
        combined_uncertainty > 0.45 ~
          "uncertainty_management_priority",
        complexity_multiplier > 1.65 ~
          "complexity_governance_priority",
        resilience_gap > 0.20 ~
          "capacity_building_priority",
        TRUE ~
          "monitor_and_learn"
      )
    ) %>%
    arrange(desc(vulnerability_weighted_systemic_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "monitoring_upgrade",
    "redundancy_and_modularity",
    "adaptive_governance",
    "deep_robustness_transition"
  ),
  probability_reduction = c(0.00, 0.02, 0.03, 0.04, 0.08),
  loss_reduction = c(0.00, 0.02, 0.06, 0.08, 0.14),
  uncertainty_reduction = c(0.00, 0.18, 0.06, 0.10, 0.18),
  dependency_reduction = c(0.00, 0.02, 0.16, 0.08, 0.20),
  monitoring_gain = c(0.00, 0.20, 0.06, 0.12, 0.20),
  redundancy_gain = c(0.00, 0.04, 0.22, 0.10, 0.24),
  flexibility_gain = c(0.00, 0.06, 0.18, 0.16, 0.24),
  learning_gain = c(0.00, 0.08, 0.08, 0.20, 0.24),
  adaptive_governance_gain = c(0.00, 0.08, 0.08, 0.22, 0.26)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    hazard_probability = pmax(0, hazard_probability * (1 - probability_reduction)),
    expected_loss_index = pmax(0, expected_loss_index * (1 - loss_reduction)),
    probability_uncertainty = pmax(0, probability_uncertainty * (1 - uncertainty_reduction)),
    loss_uncertainty = pmax(0, loss_uncertainty * (1 - uncertainty_reduction)),
    dependency_density = pmax(0, dependency_density * (1 - dependency_reduction)),
    monitoring_capacity = pmin(1, monitoring_capacity + monitoring_gain),
    redundancy_capacity = pmin(1, redundancy_capacity + redundancy_gain),
    flexibility_capacity = pmin(1, flexibility_capacity + flexibility_gain),
    institutional_learning = pmin(1, institutional_learning + learning_gain),
    adaptive_governance_capacity = pmin(1, adaptive_governance_capacity + adaptive_governance_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_expected_risk = mean(expected_risk),
    mean_uncertainty_adjusted_risk = mean(uncertainty_adjusted_risk),
    mean_complexity_multiplier = mean(complexity_multiplier),
    mean_systemic_risk = mean(vulnerability_weighted_systemic_risk),
    mean_response_capacity = mean(robust_response_capacity),
    mean_resilience_gap = mean(resilience_gap),
    elevated_risk_systems = sum(risk_band == "elevated"),
    .groups = "drop"
  ) %>%
  arrange(mean_systemic_risk)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_expected_risk = mean(expected_risk),
    mean_uncertainty_adjusted_risk = mean(uncertainty_adjusted_risk),
    mean_complexity_multiplier = mean(complexity_multiplier),
    mean_systemic_risk = mean(vulnerability_weighted_systemic_risk),
    mean_response_capacity = mean(robust_response_capacity),
    mean_resilience_gap = mean(resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_systemic_risk))

regional_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_expected_risk = mean(expected_risk),
    mean_combined_uncertainty = mean(combined_uncertainty),
    mean_complexity_multiplier = mean(complexity_multiplier),
    mean_systemic_risk = mean(vulnerability_weighted_systemic_risk),
    mean_response_capacity = mean(robust_response_capacity),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_systemic_risk))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    primary_hazard,
    expected_risk,
    combined_uncertainty,
    uncertainty_adjusted_risk,
    complexity_multiplier,
    vulnerability_weighted_systemic_risk,
    robust_response_capacity,
    resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      expected_risk,
      combined_uncertainty,
      uncertainty_adjusted_risk,
      complexity_multiplier,
      vulnerability_weighted_systemic_risk,
      robust_response_capacity,
      resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_risk_uncertainty_complexity_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_risk_uncertainty_complexity_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(regional_summary, file.path(output_dir, "r_regional_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
