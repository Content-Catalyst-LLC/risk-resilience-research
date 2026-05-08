library(readr)
library(dplyr)
library(tidyr)

base_dir <- "articles/food-system-fragility-and-resilience"
data_file <- file.path(base_dir, "data", "food_system_fragility_panel.csv")
output_dir <- file.path(base_dir, "outputs")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

systems <- read_csv(data_file, show_col_types = FALSE)

score_systems <- function(df) {
  df %>%
    mutate(
      food_system_fragility =
        0.20 * production_stress +
        0.18 * water_stress +
        0.18 * ecological_degradation +
        0.16 * logistics_fragility +
        0.14 * input_dependency +
        0.14 * price_volatility,

      food_access_vulnerability =
        0.24 * household_vulnerability +
        0.22 * price_volatility +
        0.20 * inequality_pressure +
        0.18 * (1 - social_protection_capacity) +
        0.16 * (1 - nutritional_adequacy),

      resilience_capacity =
        0.20 * food_system_diversity +
        0.18 * ecological_buffer_condition +
        0.18 * social_protection_capacity +
        0.16 * governance_capacity +
        0.14 * market_access_reliability +
        0.14 * storage_capacity,

      cascading_food_risk =
        (food_system_fragility + food_access_vulnerability) *
        (1 + 0.30 * trade_dependency) *
        (1 + 0.30 * cross_sector_linkage),

      justice_weighted_food_risk =
        cascading_food_risk *
        (1 + 0.35 * inequality_pressure),

      food_resilience_gap =
        pmax(0, justice_weighted_food_risk - resilience_capacity),

      diagnostic_priority = case_when(
        production_stress > 0.72 ~
          "production_and_climate_resilience",
        water_stress > 0.72 ~
          "water_secure_food_systems",
        ecological_degradation > 0.70 ~
          "ecological_restoration_and_soil_health",
        logistics_fragility > 0.70 ~
          "logistics_storage_and_market_continuity",
        household_vulnerability > 0.70 ~
          "social_protection_and_food_access",
        food_resilience_gap > 1.0 ~
          "close_food_resilience_gap",
        TRUE ~
          "monitor_and_preserve_food_system_resilience"
      )
    ) %>%
    arrange(desc(food_resilience_gap), desc(justice_weighted_food_risk))
}

scored <- score_systems(systems)

scenario_parameters <- tibble::tibble(
  scenario = c(
    "baseline",
    "climate_resilient_production",
    "logistics_storage_continuity",
    "social_protection_and_nutrition",
    "agroecology_and_local_diversity",
    "integrated_food_system_resilience"
  ),
  production_stress_reduction = c(0, .24, .06, .06, .18, .28),
  water_stress_reduction = c(0, .20, .06, .08, .18, .28),
  ecological_restoration_gain = c(0, .18, .06, .08, .30, .30),
  logistics_gain = c(0, .06, .30, .08, .10, .30),
  input_dependency_reduction = c(0, .10, .10, .08, .24, .28),
  price_volatility_reduction = c(0, .08, .18, .22, .10, .26),
  household_vulnerability_reduction = c(0, .06, .08, .28, .12, .30),
  inequality_reduction = c(0, .06, .08, .30, .14, .30),
  social_protection_gain = c(0, .08, .10, .32, .16, .32),
  nutritional_gain = c(0, .10, .08, .30, .18, .30),
  diversity_gain = c(0, .16, .08, .08, .34, .34),
  ecological_buffer_gain = c(0, .18, .08, .08, .32, .34),
  governance_gain = c(0, .12, .14, .18, .18, .32),
  market_access_gain = c(0, .08, .22, .12, .12, .30),
  storage_gain = c(0, .10, .30, .12, .16, .30),
  trade_dependency_reduction = c(0, .06, .10, .08, .18, .26),
  cross_sector_linkage_reduction = c(0, .06, .18, .08, .12, .24)
)

scenario_scores <- systems %>%
  tidyr::crossing(scenario_parameters) %>%
  mutate(
    production_stress = pmax(0, production_stress * (1 - production_stress_reduction)),
    water_stress = pmax(0, water_stress * (1 - water_stress_reduction)),
    ecological_degradation = pmax(0, ecological_degradation * (1 - ecological_restoration_gain)),
    logistics_fragility = pmax(0, logistics_fragility * (1 - logistics_gain)),
    input_dependency = pmax(0, input_dependency * (1 - input_dependency_reduction)),
    price_volatility = pmax(0, price_volatility * (1 - price_volatility_reduction)),
    household_vulnerability = pmax(0, household_vulnerability * (1 - household_vulnerability_reduction)),
    inequality_pressure = pmax(0, inequality_pressure * (1 - inequality_reduction)),
    social_protection_capacity = pmin(1, social_protection_capacity + social_protection_gain),
    nutritional_adequacy = pmin(1, nutritional_adequacy + nutritional_gain),
    food_system_diversity = pmin(1, food_system_diversity + diversity_gain),
    ecological_buffer_condition = pmin(1, ecological_buffer_condition + ecological_buffer_gain),
    governance_capacity = pmin(1, governance_capacity + governance_gain),
    market_access_reliability = pmin(1, market_access_reliability + market_access_gain),
    storage_capacity = pmin(1, storage_capacity + storage_gain),
    trade_dependency = pmax(0, trade_dependency * (1 - trade_dependency_reduction)),
    cross_sector_linkage = pmax(0, cross_sector_linkage * (1 - cross_sector_linkage_reduction))
  ) %>%
  group_by(scenario) %>%
  group_modify(~ score_systems(.x)) %>%
  ungroup()

scenario_summary <- scenario_scores %>%
  group_by(scenario) %>%
  summarise(
    mean_fragility = mean(food_system_fragility),
    mean_access_vulnerability = mean(food_access_vulnerability),
    mean_cascading_risk = mean(cascading_food_risk),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_resilience_gap = mean(food_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(mean_resilience_gap)

region_summary <- scored %>%
  group_by(region) %>%
  summarise(
    systems = n(),
    mean_fragility = mean(food_system_fragility),
    mean_access_vulnerability = mean(food_access_vulnerability),
    mean_cascading_risk = mean(cascading_food_risk),
    mean_resilience_capacity = mean(resilience_capacity),
    mean_resilience_gap = mean(food_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

type_summary <- scored %>%
  group_by(food_system_type) %>%
  summarise(
    systems = n(),
    mean_production_stress = mean(production_stress),
    mean_water_stress = mean(water_stress),
    mean_fragility = mean(food_system_fragility),
    mean_access_vulnerability = mean(food_access_vulnerability),
    mean_resilience_gap = mean(food_resilience_gap),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_resilience_gap))

dashboard_long <- scored %>%
  select(
    system_id,
    system_name,
    region,
    food_system_type,
    food_system_fragility,
    food_access_vulnerability,
    resilience_capacity,
    cascading_food_risk,
    justice_weighted_food_risk,
    food_resilience_gap
  ) %>%
  pivot_longer(
    cols = c(
      food_system_fragility,
      food_access_vulnerability,
      resilience_capacity,
      cascading_food_risk,
      justice_weighted_food_risk,
      food_resilience_gap
    ),
    names_to = "metric",
    values_to = "value"
  )

write_csv(scored, file.path(output_dir, "r_food_system_fragility_scores.csv"))
write_csv(scenario_scores, file.path(output_dir, "r_food_system_fragility_scenarios.csv"))
write_csv(scenario_summary, file.path(output_dir, "r_scenario_summary.csv"))
write_csv(region_summary, file.path(output_dir, "r_region_summary.csv"))
write_csv(type_summary, file.path(output_dir, "r_type_summary.csv"))
write_csv(dashboard_long, file.path(output_dir, "r_dashboard_long.csv"))

print(scored)
print(scenario_summary)
print(region_summary)
print(type_summary)
