library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/community-resilience-trust-and-local-capacity"
data_file <- file.path(base_dir, "data", "community_resilience_trust_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

communities <- read_csv(data_file, show_col_types = FALSE)

score_communities <- function(df) {
  df %>%
    mutate(
      community_hazard_pressure =
        hazard_pressure *
        exposure *
        (1 + 0.40 * social_vulnerability),

      local_resilience_capacity =
        0.16 * trust_level +
        0.15 * local_organizational_capacity +
        0.14 * mutual_aid_strength +
        0.13 * communication_access +
        0.14 * local_knowledge_integration +
        0.12 * institutional_support +
        0.08 * participation_quality +
        0.08 * recovery_capacity,

      trust_adjusted_response_capacity =
        pmin(
          1.5,
          (
            0.28 * local_organizational_capacity +
            0.25 * mutual_aid_strength +
            0.24 * communication_access +
            0.23 * local_knowledge_integration
          ) *
          (1 + 0.35 * trust_level)
        ),

      participation_legitimacy =
        pmin(
          1.5,
          participation_quality *
          (1 + 0.25 * institutional_support) *
          (1 - 0.35 * exclusion_pressure)
        ),

      community_resilience_gap =
        pmax(
          0,
          community_hazard_pressure -
          trust_adjusted_response_capacity -
          participation_legitimacy
        ),

      updated_trust_projection =
        pmin(
          1,
          pmax(
            0,
            trust_level +
            0.30 * institutional_follow_through -
            0.35 * broken_promise_pressure -
            0.20 * exclusion_pressure
          )
        ),

      diagnostic_priority = case_when(
        trust_level < 0.42 ~
          "repair_trust_and_public_accountability",
        local_organizational_capacity < 0.42 ~
          "resource_local_organizations",
        communication_access < 0.42 ~
          "strengthen_accessible_communication",
        local_knowledge_integration < 0.42 ~
          "integrate_local_and_scientific_knowledge",
        participation_quality < 0.42 ~
          "improve_participation_and_shared_authority",
        community_resilience_gap > 0.35 ~
          "close_community_resilience_gap",
        TRUE ~
          "monitor_and_strengthen_local_capacity"
      )
    ) %>%
    arrange(desc(community_resilience_gap), desc(community_hazard_pressure))
}

scored <- score_communities(communities)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "trust_and_accountability",
    "local_organization_and_mutual_aid",
    "communication_and_local_knowledge",
    "participation_and_shared_authority",
    "integrated_community_resilience"
  ),
  hazard_reduction = c(0, .04, .04, .06, .06, .18),
  exposure_reduction = c(0, .06, .08, .10, .10, .24),
  vulnerability_reduction = c(0, .08, .10, .12, .14, .30),
  trust_gain = c(0, .34, .16, .18, .22, .34),
  organizational_gain = c(0, .12, .34, .18, .20, .34),
  mutual_aid_gain = c(0, .12, .34, .16, .18, .34),
  communication_gain = c(0, .16, .20, .34, .18, .34),
  knowledge_integration_gain = c(0, .14, .18, .34, .22, .34),
  institutional_support_gain = c(0, .24, .18, .18, .32, .34),
  participation_gain = c(0, .24, .18, .20, .34, .34),
  recovery_gain = c(0, .14, .16, .16, .20, .32),
  exclusion_reduction = c(0, .28, .16, .18, .34, .34),
  follow_through_gain = c(0, .34, .18, .18, .30, .34),
  broken_promise_reduction = c(0, .34, .18, .18, .28, .34)
)

scenario_scores <- communities %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    hazard_pressure = pmax(0, hazard_pressure * (1 - hazard_reduction)),
    exposure = pmax(0, exposure * (1 - exposure_reduction)),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    trust_level = pmin(1, trust_level + trust_gain),
    local_organizational_capacity = pmin(1, local_organizational_capacity + organizational_gain),
    mutual_aid_strength = pmin(1, mutual_aid_strength + mutual_aid_gain),
    communication_access = pmin(1, communication_access + communication_gain),
    local_knowledge_integration = pmin(1, local_knowledge_integration + knowledge_integration_gain),
    institutional_support = pmin(1, institutional_support + institutional_support_gain),
    participation_quality = pmin(1, participation_quality + participation_gain),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    exclusion_pressure = pmax(0, exclusion_pressure * (1 - exclusion_reduction)),
    institutional_follow_through = pmin(1, institutional_follow_through + follow_through_gain),
    broken_promise_pressure = pmax(0, broken_promise_pressure * (1 - broken_promise_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_communities(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_hazard_pressure = mean(community_hazard_pressure),
    mean_local_capacity = mean(local_resilience_capacity),
    mean_response_capacity = mean(trust_adjusted_response_capacity),
    mean_participation_legitimacy = mean(participation_legitimacy),
    mean_resilience_gap = mean(community_resilience_gap),
    mean_updated_trust = mean(updated_trust_projection),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    communities = n(),
    mean_hazard_pressure = mean(community_hazard_pressure),
    mean_local_capacity = mean(local_resilience_capacity),
    mean_response_capacity = mean(trust_adjusted_response_capacity),
    mean_participation_legitimacy = mean(participation_legitimacy),
    mean_resilience_gap = mean(community_resilience_gap),
    mean_updated_trust = mean(updated_trust_projection),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

context_summary <- scored %>%
  group_by(risk_context) %>%
  summarise(
    communities = n(),
    mean_hazard_pressure = mean(hazard_pressure),
    mean_trust = mean(trust_level),
    mean_local_capacity = mean(local_resilience_capacity),
    mean_participation_quality = mean(participation_quality),
    mean_resilience_gap = mean(community_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    community_id,
    community_name,
    region,
    risk_context,
    community_hazard_pressure,
    local_resilience_capacity,
    trust_adjusted_response_capacity,
    participation_legitimacy,
    community_resilience_gap,
    updated_trust_projection
  ) %>%
  pivot_longer(
    cols = c(
      community_hazard_pressure,
      local_resilience_capacity,
      trust_adjusted_response_capacity,
      participation_legitimacy,
      community_resilience_gap,
      updated_trust_projection
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_community_resilience_trust_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_community_resilience_trust_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(context_summary)
