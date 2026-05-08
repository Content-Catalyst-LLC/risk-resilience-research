library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/resilience-robustness-antifragility"
data_file <- file.path(base_dir, "data", "resilience_robustness_antifragility_panel.csv")
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
      stress_load =
        stress_intensity *
        (1 + 0.5 * stress_variability) *
        (1 + 0.4 * system_criticality),

      robustness_score = robustness_capacity,

      resilience_score =
        0.23 * recovery_capacity +
        0.22 * adaptive_capacity +
        0.18 * redundancy_capacity +
        0.16 * modularity_capacity +
        0.11 * monitoring_capacity +
        0.10 * failure_containment,

      antifragility_potential =
        0.24 * learning_capacity +
        0.22 * experimentation_capacity +
        0.20 * optionality_capacity +
        0.16 * modularity_capacity +
        0.10 * failure_containment +
        0.08 * monitoring_capacity,

      ethical_antifragility_limit =
        0.42 * harm_bounding_capacity +
        0.36 * justice_safeguard_capacity +
        0.22 * failure_containment,

      bounded_antifragility_score =
        antifragility_potential * ethical_antifragility_limit,

      brittleness_risk =
        pmax(
          0,
          stress_load -
            (
              0.42 * robustness_score +
              0.38 * resilience_score +
              0.20 * ethical_antifragility_limit
            )
        ),

      sustainable_resilience_score =
        0.30 * robustness_score +
        0.42 * resilience_score +
        0.18 * bounded_antifragility_score +
        0.10 * justice_safeguard_capacity,

      system_response_gap =
        pmax(0, stress_load - sustainable_resilience_score),

      antifragility_suitability =
        pmin(
          1,
          bounded_antifragility_score *
            (1 - 0.55 * system_criticality) *
            failure_containment
        ),

      design_priority = case_when(
        system_criticality > 0.80 ~
          "robustness_for_critical_lifeline",
        brittleness_risk > 0.35 ~
          "resilience_and_brittleness_reduction",
        antifragility_suitability > 0.20 ~
          "bounded_antifragile_learning",
        system_response_gap > 0.30 ~
          "adaptive_resilience_upgrade",
        TRUE ~
          "balanced_monitoring_and_maintenance"
      ),

      stress_band = classify_band(stress_load, 0.80, 1.25),
      response_band = classify_band(sustainable_resilience_score, 0.40, 0.65)
    ) %>%
    arrange(desc(system_response_gap), desc(brittleness_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "robustness_upgrade",
    "resilience_upgrade",
    "bounded_antifragility",
    "sustainable_resilience_portfolio"
  ),
  stress_reduction = c(0.00, 0.04, 0.04, 0.02, 0.08),
  robustness_gain = c(0.00, 0.24, 0.08, 0.04, 0.16),
  recovery_gain = c(0.00, 0.06, 0.20, 0.08, 0.20),
  adaptive_gain = c(0.00, 0.04, 0.18, 0.16, 0.20),
  redundancy_gain = c(0.00, 0.06, 0.18, 0.10, 0.20),
  modularity_gain = c(0.00, 0.04, 0.16, 0.18, 0.22),
  learning_gain = c(0.00, 0.04, 0.12, 0.24, 0.22),
  experimentation_gain = c(0.00, 0.02, 0.08, 0.26, 0.18),
  optionality_gain = c(0.00, 0.02, 0.08, 0.24, 0.20),
  containment_gain = c(0.00, 0.08, 0.14, 0.22, 0.24),
  justice_gain = c(0.00, 0.06, 0.12, 0.18, 0.24)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    stress_intensity = pmax(0, stress_intensity * (1 - stress_reduction)),
    robustness_capacity = pmin(1, robustness_capacity + robustness_gain),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    adaptive_capacity = pmin(1, adaptive_capacity + adaptive_gain),
    redundancy_capacity = pmin(1, redundancy_capacity + redundancy_gain),
    modularity_capacity = pmin(1, modularity_capacity + modularity_gain),
    learning_capacity = pmin(1, learning_capacity + learning_gain),
    experimentation_capacity = pmin(1, experimentation_capacity + experimentation_gain),
    optionality_capacity = pmin(1, optionality_capacity + optionality_gain),
    failure_containment = pmin(1, failure_containment + containment_gain),
    harm_bounding_capacity = pmin(1, harm_bounding_capacity + containment_gain),
    justice_safeguard_capacity = pmin(1, justice_safeguard_capacity + justice_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_stress_load = mean(stress_load),
    mean_robustness = mean(robustness_score),
    mean_resilience = mean(resilience_score),
    mean_bounded_antifragility = mean(bounded_antifragility_score),
    mean_brittleness_risk = mean(brittleness_risk),
    mean_sustainable_resilience = mean(sustainable_resilience_score),
    mean_response_gap = mean(system_response_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_response_gap)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_stress_load = mean(stress_load),
    mean_robustness = mean(robustness_score),
    mean_resilience = mean(resilience_score),
    mean_bounded_antifragility = mean(bounded_antifragility_score),
    mean_brittleness_risk = mean(brittleness_risk),
    mean_sustainable_resilience = mean(sustainable_resilience_score),
    mean_response_gap = mean(system_response_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_response_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    stress_type,
    stress_load,
    robustness_score,
    resilience_score,
    bounded_antifragility_score,
    brittleness_risk,
    sustainable_resilience_score,
    system_response_gap,
    antifragility_suitability
  ) %>%
  pivot_longer(
    cols = c(
      stress_load,
      robustness_score,
      resilience_score,
      bounded_antifragility_score,
      brittleness_risk,
      sustainable_resilience_score,
      system_response_gap,
      antifragility_suitability
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_resilience_robustness_antifragility_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_resilience_robustness_antifragility_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
