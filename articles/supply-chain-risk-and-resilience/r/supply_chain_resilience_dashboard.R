library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/supply-chain-risk-and-resilience"
data_file <- file.path(base_dir, "data", "supply_chain_resilience_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

items <- read_csv(data_file, show_col_types = FALSE)

score_supply_chains <- function(df) {
  df %>%
    mutate(
      disruption_pressure =
        criticality *
        (
          0.22 * supplier_concentration +
          0.20 * dependency_intensity +
          0.18 * logistics_exposure +
          0.16 * cyber_digital_risk +
          0.14 * workforce_vulnerability +
          0.10 * climate_hazard_exposure
        ),

      resilience_buffer_capacity =
        0.22 * inventory_buffer +
        0.20 * substitutability +
        0.20 * supplier_redundancy +
        0.16 * modular_production_capacity +
        0.12 * governance_capacity +
        0.10 * logistics_flexibility,

      shortage_risk =
        disruption_pressure *
        (1 + 0.40 * recovery_time_pressure) *
        (1 - 0.45 * resilience_buffer_capacity),

      concentration_adjusted_dependency =
        supplier_concentration *
        dependency_intensity *
        (1 - substitutability),

      service_continuity_gap =
        pmax(
          0,
          criticality + shortage_risk - resilience_buffer_capacity
        ),

      public_priority_score =
        service_continuity_gap +
        0.30 * criticality +
        0.25 * vulnerable_population_exposure +
        0.25 * essential_service_relevance,

      diagnostic_priority = case_when(
        supplier_concentration > 0.70 ~
          "reduce_supplier_concentration",
        logistics_exposure > 0.70 ~
          "diversify_logistics_routes_and_chokepoints",
        inventory_buffer < 0.35 ~
          "increase_inventory_or_strategic_reserves",
        substitutability < 0.35 ~
          "improve_substitutability_and_standards",
        supplier_redundancy < 0.35 ~
          "expand_supplier_redundancy",
        service_continuity_gap > 0.75 ~
          "close_service_continuity_gap",
        TRUE ~
          "monitor_and_strengthen_supply_chain_resilience"
      )
    ) %>%
    arrange(desc(public_priority_score), desc(service_continuity_gap))
}

scored <- score_supply_chains(items)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "supplier_diversification",
    "inventory_and_strategic_reserves",
    "logistics_and_chokepoint_resilience",
    "digital_and_workforce_resilience",
    "integrated_supply_chain_resilience"
  ),
  concentration_reduction = c(0, .34, .08, .10, .08, .34),
  dependency_reduction = c(0, .24, .10, .12, .10, .34),
  logistics_exposure_reduction = c(0, .10, .08, .34, .12, .34),
  cyber_risk_reduction = c(0, .08, .06, .12, .34, .34),
  workforce_vulnerability_reduction = c(0, .08, .06, .10, .30, .30),
  climate_exposure_reduction = c(0, .08, .06, .20, .08, .30),
  inventory_gain = c(0, .12, .34, .16, .12, .34),
  substitutability_gain = c(0, .18, .12, .14, .14, .34),
  supplier_redundancy_gain = c(0, .34, .14, .18, .16, .34),
  modularity_gain = c(0, .16, .10, .16, .18, .34),
  governance_gain = c(0, .18, .18, .20, .24, .34),
  logistics_flexibility_gain = c(0, .14, .12, .34, .18, .34),
  recovery_time_reduction = c(0, .18, .26, .20, .18, .34),
  vulnerable_exposure_reduction = c(0, .08, .10, .12, .16, .26)
)

scenario_scores <- list()

for (i in seq_len(nrow(scenario_parameters))) {
  p <- scenario_parameters[i, ]

  scenario_items <- items %>%
    mutate(
      supplier_concentration = pmax(0, supplier_concentration * (1 - p$concentration_reduction)),
      dependency_intensity = pmax(0, dependency_intensity * (1 - p$dependency_reduction)),
      logistics_exposure = pmax(0, logistics_exposure * (1 - p$logistics_exposure_reduction)),
      cyber_digital_risk = pmax(0, cyber_digital_risk * (1 - p$cyber_risk_reduction)),
      workforce_vulnerability = pmax(0, workforce_vulnerability * (1 - p$workforce_vulnerability_reduction)),
      climate_hazard_exposure = pmax(0, climate_hazard_exposure * (1 - p$climate_exposure_reduction)),
      inventory_buffer = pmin(1, inventory_buffer + p$inventory_gain),
      substitutability = pmin(1, substitutability + p$substitutability_gain),
      supplier_redundancy = pmin(1, supplier_redundancy + p$supplier_redundancy_gain),
      modular_production_capacity = pmin(1, modular_production_capacity + p$modularity_gain),
      governance_capacity = pmin(1, governance_capacity + p$governance_gain),
      logistics_flexibility = pmin(1, logistics_flexibility + p$logistics_flexibility_gain),
      recovery_time_pressure = pmax(0, recovery_time_pressure * (1 - p$recovery_time_reduction)),
      vulnerable_population_exposure = pmax(0, vulnerable_population_exposure * (1 - p$vulnerable_exposure_reduction))
    )

  scenario_scores[[i]] <- score_supply_chains(scenario_items) %>%
    mutate(scenario = p$scenario)
}

scenario_scores <- bind_rows(scenario_scores)

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_disruption_pressure = mean(disruption_pressure),
    mean_buffer_capacity = mean(resilience_buffer_capacity),
    mean_shortage_risk = mean(shortage_risk),
    mean_dependency = mean(concentration_adjusted_dependency),
    mean_continuity_gap = mean(service_continuity_gap),
    mean_public_priority = mean(public_priority_score),
    .groups = "drop"
  ) %>%
  arrange(mean_public_priority)

sector_summary <- scored %>%
  group_by(sector) %>%
  summarise(
    items = n(),
    mean_disruption_pressure = mean(disruption_pressure),
    mean_buffer_capacity = mean(resilience_buffer_capacity),
    mean_shortage_risk = mean(shortage_risk),
    mean_dependency = mean(concentration_adjusted_dependency),
    mean_continuity_gap = mean(service_continuity_gap),
    mean_public_priority = mean(public_priority_score),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_public_priority))

context_summary <- scored %>%
  group_by(supply_context) %>%
  summarise(
    items = n(),
    mean_criticality = mean(criticality),
    mean_supplier_concentration = mean(supplier_concentration),
    mean_logistics_exposure = mean(logistics_exposure),
    mean_buffer_capacity = mean(resilience_buffer_capacity),
    mean_continuity_gap = mean(service_continuity_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_continuity_gap))

dashboard_long <- scored %>%
  select(
    item_id,
    item_name,
    sector,
    supply_context,
    disruption_pressure,
    resilience_buffer_capacity,
    shortage_risk,
    concentration_adjusted_dependency,
    service_continuity_gap,
    public_priority_score
  ) %>%
  pivot_longer(
    cols = c(
      disruption_pressure,
      resilience_buffer_capacity,
      shortage_risk,
      concentration_adjusted_dependency,
      service_continuity_gap,
      public_priority_score
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_supply_chain_resilience_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_supply_chain_resilience_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(sector_summary, file.path(output_dir, "r_sector_summary.csv"))
write_csv(context_summary, file.path(output_dir, "r_context_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(sector_summary)
print(context_summary)
