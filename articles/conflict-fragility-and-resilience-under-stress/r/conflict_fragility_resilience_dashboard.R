library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/conflict-fragility-and-resilience-under-stress"
data_file <- file.path(base_dir, "data", "conflict_fragility_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      fragility_pressure =
        0.24 * conflict_intensity +
        0.20 * social_vulnerability +
        0.18 * displacement_pressure +
        0.18 * livelihood_stress +
        0.20 * hazard_exposure,

      governance_resilience =
        0.24 * governance_capacity +
        0.22 * service_continuity +
        0.20 * institutional_legitimacy +
        0.18 * administrative_reach +
        0.16 * recovery_capacity,

      conflict_amplified_systemic_risk =
        fragility_pressure *
        (1 + 0.45 * conflict_intensity) *
        (1 - 0.35 * governance_resilience),

      service_breakdown_gap =
        pmax(0, essential_service_demand - service_continuity),

      legitimacy_erosion =
        pmin(
          1.5,
          pmax(
            0,
            0.30 * service_breakdown_gap +
            0.26 * inequality_pressure +
            0.24 * institutional_exclusion +
            0.15 * repeated_disruption_pressure -
            0.20 * public_trust
          )
        ),

      resilience_under_stress_gap =
        pmax(
          0,
          conflict_amplified_systemic_risk +
          service_breakdown_gap +
          legitimacy_erosion -
          governance_resilience
        ),

      diagnostic_priority = case_when(
        conflict_intensity > 0.72 ~
          "conflict_prevention_and_protection",
        service_continuity < 0.42 ~
          "restore_essential_service_continuity",
        institutional_legitimacy < 0.42 ~
          "repair_legitimacy_and_public_trust",
        administrative_reach < 0.42 ~
          "strengthen_administrative_reach",
        displacement_pressure > 0.70 ~
          "protect_displaced_people_and_livelihoods",
        resilience_under_stress_gap > 0.75 ~
          "close_resilience_under_stress_gap",
        TRUE ~
          "monitor_and_strengthen_fragility_resilience"
      )
    ) %>%
    arrange(desc(resilience_under_stress_gap), desc(conflict_amplified_systemic_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "service_continuity_and_protection",
    "local_governance_and_legitimacy",
    "displacement_and_livelihood_resilience",
    "fragility_aware_early_warning",
    "integrated_resilience_under_stress"
  ),
  conflict_reduction = c(0, .08, .10, .08, .08, .24),
  governance_gain = c(0, .12, .26, .14, .20, .34),
  service_gain = c(0, .30, .18, .16, .20, .34),
  legitimacy_gain = c(0, .16, .32, .16, .18, .34),
  administrative_reach_gain = c(0, .14, .28, .16, .22, .34),
  recovery_gain = c(0, .18, .18, .28, .22, .34),
  vulnerability_reduction = c(0, .12, .10, .18, .12, .30),
  displacement_reduction = c(0, .12, .10, .32, .12, .34),
  livelihood_stress_reduction = c(0, .10, .12, .34, .12, .32),
  hazard_exposure_reduction = c(0, .08, .06, .10, .24, .28),
  service_demand_reduction = c(0, .20, .10, .18, .22, .30),
  inequality_reduction = c(0, .12, .20, .18, .14, .32),
  exclusion_reduction = c(0, .12, .28, .16, .14, .32),
  trust_gain = c(0, .16, .34, .18, .20, .34),
  repeated_disruption_reduction = c(0, .12, .14, .22, .24, .30)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    conflict_intensity = pmax(0, conflict_intensity * (1 - conflict_reduction)),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    service_continuity = pmin(1, service_continuity + service_gain),
    institutional_legitimacy = pmin(1, institutional_legitimacy + legitimacy_gain),
    administrative_reach = pmin(1, administrative_reach + administrative_reach_gain),
    recovery_capacity = pmin(1, recovery_capacity + recovery_gain),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    displacement_pressure = pmax(0, displacement_pressure * (1 - displacement_reduction)),
    livelihood_stress = pmax(0, livelihood_stress * (1 - livelihood_stress_reduction)),
    hazard_exposure = pmax(0, hazard_exposure * (1 - hazard_exposure_reduction)),
    essential_service_demand = pmax(0, essential_service_demand * (1 - service_demand_reduction)),
    inequality_pressure = pmax(0, inequality_pressure * (1 - inequality_reduction)),
    institutional_exclusion = pmax(0, institutional_exclusion * (1 - exclusion_reduction)),
    public_trust = pmin(1, public_trust + trust_gain),
    repeated_disruption_pressure = pmax(0, repeated_disruption_pressure * (1 - repeated_disruption_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_fragility_pressure = mean(fragility_pressure),
    mean_governance_resilience = mean(governance_resilience),
    mean_systemic_risk = mean(conflict_amplified_systemic_risk),
    mean_service_gap = mean(service_breakdown_gap),
    mean_resilience_gap = mean(resilience_under_stress_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_fragility_pressure = mean(fragility_pressure),
    mean_governance_resilience = mean(governance_resilience),
    mean_systemic_risk = mean(conflict_amplified_systemic_risk),
    mean_service_gap = mean(service_breakdown_gap),
    mean_resilience_gap = mean(resilience_under_stress_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

context_summary <- scored %>%
  group_by(fragility_context) %>%
  summarise(
    systems = n(),
    mean_conflict_intensity = mean(conflict_intensity),
    mean_service_continuity = mean(service_continuity),
    mean_legitimacy = mean(institutional_legitimacy),
    mean_fragility_pressure = mean(fragility_pressure),
    mean_resilience_gap = mean(resilience_under_stress_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    fragility_context,
    fragility_pressure,
    governance_resilience,
    conflict_amplified_systemic_risk,
    service_breakdown_gap,
    legitimacy_erosion,
    resilience_under_stress_gap
  ) %>%
  pivot_longer(
    cols = c(
      fragility_pressure,
      governance_resilience,
      conflict_amplified_systemic_risk,
      service_breakdown_gap,
      legitimacy_erosion,
      resilience_under_stress_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_conflict_fragility_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_conflict_fragility_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(context_summary)
