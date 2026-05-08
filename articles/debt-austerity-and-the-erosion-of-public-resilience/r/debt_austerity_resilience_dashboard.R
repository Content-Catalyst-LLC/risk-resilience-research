library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/debt-austerity-and-the-erosion-of-public-resilience"
data_file <- file.path(base_dir, "data", "debt_austerity_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      debt_service_pressure =
        pmin(1.5, debt_service_burden / (0.20 + revenue_capacity)),

      public_resilience_capacity =
        0.18 * essential_service_spending +
        0.16 * public_investment +
        0.15 * maintenance_capacity +
        0.16 * adaptation_drr_spending +
        0.15 * social_protection_capacity +
        0.12 * governance_capacity +
        0.08 * local_government_capacity,

      austerity_intensity =
        0.20 * essential_service_cuts +
        0.20 * public_investment_cuts +
        0.18 * maintenance_deferral +
        0.18 * adaptation_deferral +
        0.16 * social_protection_cuts +
        0.08 * public_workforce_stress,

      fiscal_resilience_risk =
        (debt_service_pressure + austerity_intensity) *
        (1 + 0.35 * social_vulnerability) *
        (1 + 0.30 * hazard_exposure) *
        (1 + 0.25 * inequality_pressure) *
        (1 - 0.45 * public_resilience_capacity),

      deferred_risk_burden =
        pmin(
          1.5,
          pmax(
            0,
            prior_deferred_risk +
            0.40 * austerity_intensity -
            0.20 * public_investment -
            0.20 * maintenance_capacity -
            0.20 * adaptation_drr_spending
          )
        ),

      public_resilience_gap =
        pmax(
          0,
          fiscal_resilience_risk +
          deferred_risk_burden -
          public_resilience_capacity
        ),

      diagnostic_priority = case_when(
        debt_service_pressure > 0.85 ~
          "debt_restructuring_or_debt_service_relief",
        essential_service_cuts > 0.65 ~
          "protect_essential_services",
        maintenance_deferral > 0.65 ~
          "restore_maintenance_and_infrastructure_capacity",
        adaptation_deferral > 0.65 ~
          "protect_climate_adaptation_and_drr",
        social_protection_cuts > 0.65 ~
          "protect_social_protection_and_care_systems",
        public_resilience_gap > 0.75 ~
          "close_public_resilience_gap",
        TRUE ~
          "monitor_and_strengthen_fiscal_resilience"
      )
    ) %>%
    arrange(desc(public_resilience_gap), desc(fiscal_resilience_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "debt_relief_and_revenue_reform",
    "protect_essential_services",
    "restore_maintenance_and_adaptation",
    "social_protection_and_local_capacity",
    "integrated_fiscal_resilience"
  ),
  debt_service_reduction = c(0, .34, .12, .10, .10, .34),
  revenue_capacity_gain = c(0, .30, .14, .14, .18, .34),
  essential_spending_gain = c(0, .12, .34, .16, .18, .34),
  public_investment_gain = c(0, .14, .14, .28, .16, .34),
  maintenance_gain = c(0, .12, .16, .34, .18, .34),
  adaptation_gain = c(0, .14, .14, .34, .16, .34),
  social_protection_gain = c(0, .16, .28, .16, .34, .34),
  governance_gain = c(0, .16, .18, .16, .22, .34),
  local_government_gain = c(0, .14, .18, .22, .34, .34),
  essential_cuts_reduction = c(0, .16, .34, .14, .20, .34),
  investment_cuts_reduction = c(0, .18, .16, .28, .18, .34),
  maintenance_deferral_reduction = c(0, .18, .16, .34, .18, .34),
  adaptation_deferral_reduction = c(0, .18, .16, .34, .18, .34),
  social_protection_cuts_reduction = c(0, .18, .30, .14, .34, .34),
  workforce_stress_reduction = c(0, .16, .24, .18, .24, .34),
  vulnerability_reduction = c(0, .10, .22, .12, .30, .34),
  hazard_exposure_reduction = c(0, .08, .08, .28, .10, .30),
  inequality_reduction = c(0, .18, .22, .12, .30, .34),
  deferred_risk_reduction = c(0, .12, .14, .30, .18, .34)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    debt_service_burden = pmax(0, debt_service_burden * (1 - debt_service_reduction)),
    revenue_capacity = pmin(1, revenue_capacity + revenue_capacity_gain),
    essential_service_spending = pmin(1, essential_service_spending + essential_spending_gain),
    public_investment = pmin(1, public_investment + public_investment_gain),
    maintenance_capacity = pmin(1, maintenance_capacity + maintenance_gain),
    adaptation_drr_spending = pmin(1, adaptation_drr_spending + adaptation_gain),
    social_protection_capacity = pmin(1, social_protection_capacity + social_protection_gain),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    local_government_capacity = pmin(1, local_government_capacity + local_government_gain),
    essential_service_cuts = pmax(0, essential_service_cuts * (1 - essential_cuts_reduction)),
    public_investment_cuts = pmax(0, public_investment_cuts * (1 - investment_cuts_reduction)),
    maintenance_deferral = pmax(0, maintenance_deferral * (1 - maintenance_deferral_reduction)),
    adaptation_deferral = pmax(0, adaptation_deferral * (1 - adaptation_deferral_reduction)),
    social_protection_cuts = pmax(0, social_protection_cuts * (1 - social_protection_cuts_reduction)),
    public_workforce_stress = pmax(0, public_workforce_stress * (1 - workforce_stress_reduction)),
    social_vulnerability = pmax(0, social_vulnerability * (1 - vulnerability_reduction)),
    hazard_exposure = pmax(0, hazard_exposure * (1 - hazard_exposure_reduction)),
    inequality_pressure = pmax(0, inequality_pressure * (1 - inequality_reduction)),
    prior_deferred_risk = pmax(0, prior_deferred_risk * (1 - deferred_risk_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_debt_pressure = mean(debt_service_pressure),
    mean_austerity = mean(austerity_intensity),
    mean_public_capacity = mean(public_resilience_capacity),
    mean_fiscal_risk = mean(fiscal_resilience_risk),
    mean_deferred_risk = mean(deferred_risk_burden),
    mean_resilience_gap = mean(public_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_debt_pressure = mean(debt_service_pressure),
    mean_austerity = mean(austerity_intensity),
    mean_public_capacity = mean(public_resilience_capacity),
    mean_fiscal_risk = mean(fiscal_resilience_risk),
    mean_deferred_risk = mean(deferred_risk_burden),
    mean_resilience_gap = mean(public_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

context_summary <- scored %>%
  group_by(fiscal_context) %>%
  summarise(
    systems = n(),
    mean_debt_service_burden = mean(debt_service_burden),
    mean_revenue_capacity = mean(revenue_capacity),
    mean_austerity = mean(austerity_intensity),
    mean_public_capacity = mean(public_resilience_capacity),
    mean_resilience_gap = mean(public_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    fiscal_context,
    debt_service_pressure,
    austerity_intensity,
    public_resilience_capacity,
    fiscal_resilience_risk,
    deferred_risk_burden,
    public_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      debt_service_pressure,
      austerity_intensity,
      public_resilience_capacity,
      fiscal_resilience_risk,
      deferred_risk_burden,
      public_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_debt_austerity_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_debt_austerity_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(context_summary)
