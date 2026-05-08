library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/adaptation-recovery-transformation"
data_file <- file.path(base_dir, "data", "adaptation_recovery_transformation_panel.csv")
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
      recovery_score =
        0.38 * recovery_capacity +
        0.28 * recovery_speed +
        0.34 * essential_function_restoration,

      adaptation_score =
        0.26 * adaptive_capacity +
        0.22 * governance_capacity +
        0.18 * learning_capacity +
        0.18 * ecological_buffer_capacity +
        0.16 * social_protection_capacity,

      transformation_need =
        0.36 * structural_unsustainability +
        0.26 * justice_pressure +
        0.22 * residual_risk +
        0.16 * maladaptation_risk,

      transformation_score =
        0.34 * transformation_readiness +
        0.22 * governance_capacity +
        0.18 * learning_capacity +
        0.14 * public_legitimacy +
        0.12 * social_protection_capacity,

      response_capacity =
        0.28 * recovery_score +
        0.36 * adaptation_score +
        0.24 * transformation_score +
        0.12 * public_legitimacy,

      pathway_gap =
        pmax(0, disruption_severity + residual_risk - response_capacity),

      maladaptation_adjusted_gap =
        pathway_gap * (1 + maladaptation_risk),

      transformational_threshold =
        pmax(0, transformation_need - transformation_score),

      climate_resilient_development_score =
        pmin(
          1,
          0.24 * recovery_score +
            0.30 * adaptation_score +
            0.26 * transformation_score +
            0.12 * public_legitimacy +
            0.08 * (1 - maladaptation_risk)
        ),

      response_priority = case_when(
        disruption_severity > 0.78 ~
          "urgent_recovery_with_risk_reduction",
        transformational_threshold > 0.22 ~
          "transformation_planning_priority",
        maladaptation_risk > 0.55 ~
          "maladaptation_avoidance_priority",
        adaptation_score < 0.48 ~
          "adaptive_capacity_building",
        TRUE ~
          "maintain_and_monitor_pathway"
      ),

      recovery_band = classify_band(recovery_score, 0.40, 0.65),
      adaptation_band = classify_band(adaptation_score, 0.40, 0.65),
      transformation_need_band = classify_band(transformation_need, 0.35, 0.60)
    ) %>%
    arrange(desc(maladaptation_adjusted_gap), desc(transformational_threshold))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "recovery_upgrade",
    "adaptive_pathways",
    "justice_centered_transformation",
    "climate_resilient_development"
  ),
  disruption_reduction = c(0.00, 0.02, 0.04, 0.06, 0.10),
  recovery_gain = c(0.00, 0.22, 0.08, 0.10, 0.18),
  adaptation_gain = c(0.00, 0.06, 0.22, 0.16, 0.24),
  governance_gain = c(0.00, 0.08, 0.16, 0.20, 0.24),
  learning_gain = c(0.00, 0.06, 0.18, 0.20, 0.24),
  ecological_buffer_gain = c(0.00, 0.04, 0.14, 0.18, 0.24),
  social_protection_gain = c(0.00, 0.10, 0.12, 0.22, 0.24),
  transformation_gain = c(0.00, 0.04, 0.10, 0.28, 0.26),
  maladaptation_reduction = c(0.00, 0.04, 0.12, 0.20, 0.24),
  legitimacy_gain = c(0.00, 0.08, 0.12, 0.22, 0.24)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    disruption_severity = pmax(0, disruption_severity * (1 - disruption_reduction)),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    recovery_speed = pmin(1, recovery_speed + recovery_gain),
    essential_function_restoration = pmin(1, essential_function_restoration + recovery_gain),
    adaptive_capacity = pmin(1, adaptive_capacity + adaptation_gain),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    learning_capacity = pmin(1, learning_capacity + learning_gain),
    ecological_buffer_capacity = pmin(1, ecological_buffer_capacity + ecological_buffer_gain),
    social_protection_capacity = pmin(1, social_protection_capacity + social_protection_gain),
    transformation_readiness = pmin(1, transformation_readiness + transformation_gain),
    maladaptation_risk = pmax(0, maladaptation_risk * (1 - maladaptation_reduction)),
    public_legitimacy = pmin(1, public_legitimacy + legitimacy_gain)
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_recovery = mean(recovery_score),
    mean_adaptation = mean(adaptation_score),
    mean_transformation = mean(transformation_score),
    mean_transformation_need = mean(transformation_need),
    mean_pathway_gap = mean(pathway_gap),
    mean_maladaptation_gap = mean(maladaptation_adjusted_gap),
    mean_crd_score = mean(climate_resilient_development_score),
    .groups = "drop"
  ) %>%
  arrange(mean_maladaptation_gap)

domain_summary <- scored %>%
  group_by(domain) %>%
  summarise(
    systems = n(),
    mean_recovery = mean(recovery_score),
    mean_adaptation = mean(adaptation_score),
    mean_transformation = mean(transformation_score),
    mean_transformation_need = mean(transformation_need),
    mean_pathway_gap = mean(pathway_gap),
    mean_maladaptation_gap = mean(maladaptation_adjusted_gap),
    mean_crd_score = mean(climate_resilient_development_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_maladaptation_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    domain,
    region,
    stress_type,
    recovery_score,
    adaptation_score,
    transformation_score,
    transformation_need,
    pathway_gap,
    maladaptation_adjusted_gap,
    climate_resilient_development_score
  ) %>%
  pivot_longer(
    cols = c(
      recovery_score,
      adaptation_score,
      transformation_score,
      transformation_need,
      pathway_gap,
      maladaptation_adjusted_gap,
      climate_resilient_development_score
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_adaptation_recovery_transformation_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_adaptation_recovery_transformation_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(domain_summary, file.path(output_dir, "r_domain_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(domain_summary)
