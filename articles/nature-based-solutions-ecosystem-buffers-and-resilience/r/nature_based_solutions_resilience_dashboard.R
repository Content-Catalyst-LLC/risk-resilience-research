library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/nature-based-solutions-ecosystem-buffers-and-resilience"
data_file <- file.path(base_dir, "data", "nature_based_solutions_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

projects <- read_csv(data_file, show_col_types = FALSE)

score_projects <- function(df) {
  df %>%
    mutate(
      nbs_integrity =
        0.20 * ecosystem_condition +
        0.18 * biodiversity_benefit +
        0.16 * ecological_connectivity +
        0.16 * intervention_quality +
        0.15 * governance_capacity +
        0.15 * maintenance_capacity,

      hazard_vulnerability_pressure =
        hazard_pressure *
        exposure *
        (1 + 0.35 * social_vulnerability),

      buffer_effectiveness =
        pmin(
          1.5,
          nbs_integrity *
            (1 + 0.22 * social_legitimacy) *
            (1 + 0.18 * livelihood_benefit)
        ),

      nature_adjusted_risk =
        hazard_vulnerability_pressure *
        (1 - 0.45 * pmin(1, buffer_effectiveness)) *
        (1 - 0.25 * governance_capacity),

      credibility_risk =
        0.22 * (1 - ecosystem_condition) +
        0.20 * (1 - biodiversity_benefit) +
        0.18 * (1 - social_legitimacy) +
        0.18 * (1 - maintenance_capacity) +
        0.22 * displacement_pressure,

      justice_weighted_nbs_risk =
        (nature_adjusted_risk + credibility_risk) *
        (1 + 0.30 * social_vulnerability),

      nbs_resilience_gap =
        pmax(0, justice_weighted_nbs_risk - buffer_effectiveness),

      diagnostic_priority = case_when(
        ecosystem_condition < 0.42 ~
          "restore_ecological_condition",
        biodiversity_benefit < 0.42 ~
          "strengthen_biodiversity_benefits",
        social_legitimacy < 0.42 ~
          "repair_social_legitimacy_and_rights",
        maintenance_capacity < 0.42 ~
          "fund_long_term_maintenance",
        displacement_pressure > 0.62 ~
          "reduce_displacement_and_green_gentrification_risk",
        nbs_resilience_gap > 0.45 ~
          "close_nature_based_resilience_gap",
        TRUE ~
          "monitor_and_preserve_nbs_performance"
      )
    ) %>%
    arrange(desc(nbs_resilience_gap), desc(justice_weighted_nbs_risk))
}

scored <- score_projects(projects)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "ecological_integrity",
    "governance_and_maintenance",
    "rights_and_social_legitimacy",
    "hazard_buffer_performance",
    "integrated_nature_based_resilience"
  ),
  ecosystem_condition_gain = c(0, .24, .10, .08, .18, .30),
  biodiversity_gain = c(0, .30, .10, .10, .18, .32),
  connectivity_gain = c(0, .24, .12, .08, .20, .30),
  intervention_quality_gain = c(0, .20, .18, .14, .24, .30),
  governance_gain = c(0, .10, .30, .24, .18, .32),
  maintenance_gain = c(0, .12, .30, .16, .18, .32),
  hazard_reduction = c(0, .06, .06, .06, .22, .24),
  exposure_reduction = c(0, .04, .08, .12, .20, .24),
  vulnerability_reduction = c(0, .06, .08, .26, .12, .30),
  legitimacy_gain = c(0, .08, .18, .34, .14, .34),
  livelihood_gain = c(0, .08, .10, .24, .12, .30),
  displacement_reduction = c(0, .06, .12, .34, .12, .34)
)

scenario_scores <- projects %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    ecosystem_condition = pmin(1, ecosystem_condition + ecosystem_condition_gain),
    biodiversity_benefit = pmin(1, biodiversity_benefit + biodiversity_gain),
    ecological_connectivity = pmin(1, ecological_connectivity + connectivity_gain),
    intervention_quality = pmin(1, intervention_quality + intervention_quality_gain),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    maintenance_capacity = pmin(1, maintenance_capacity + maintenance_gain),
    hazard_pressure = pmax(0, hazard_pressure * (1 - hazard_reduction)),
    exposure = pmax(0, exposure * (1 - exposure_reduction)),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    social_legitimacy = pmin(1, social_legitimacy + legitimacy_gain),
    livelihood_benefit = pmin(1, livelihood_benefit + livelihood_gain),
    displacement_pressure = pmax(0, displacement_pressure * (1 - displacement_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_projects(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_integrity = mean(nbs_integrity),
    mean_buffer_effectiveness = mean(buffer_effectiveness),
    mean_nature_adjusted_risk = mean(nature_adjusted_risk),
    mean_credibility_risk = mean(credibility_risk),
    mean_resilience_gap = mean(nbs_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    projects = n(),
    mean_integrity = mean(nbs_integrity),
    mean_buffer_effectiveness = mean(buffer_effectiveness),
    mean_nature_adjusted_risk = mean(nature_adjusted_risk),
    mean_credibility_risk = mean(credibility_risk),
    mean_resilience_gap = mean(nbs_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

type_summary <- scored %>%
  group_by(solution_type) %>%
  summarise(
    projects = n(),
    mean_ecosystem_condition = mean(ecosystem_condition),
    mean_biodiversity_benefit = mean(biodiversity_benefit),
    mean_social_legitimacy = mean(social_legitimacy),
    mean_buffer_effectiveness = mean(buffer_effectiveness),
    mean_resilience_gap = mean(nbs_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    project_id,
    project_name,
    region,
    solution_type,
    nbs_integrity,
    hazard_vulnerability_pressure,
    buffer_effectiveness,
    nature_adjusted_risk,
    credibility_risk,
    justice_weighted_nbs_risk,
    nbs_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      nbs_integrity,
      hazard_vulnerability_pressure,
      buffer_effectiveness,
      nature_adjusted_risk,
      credibility_risk,
      justice_weighted_nbs_risk,
      nbs_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_nature_based_solution_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_nature_based_solution_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(type_summary, file.path(output_dir, "r_type_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(type_summary)
