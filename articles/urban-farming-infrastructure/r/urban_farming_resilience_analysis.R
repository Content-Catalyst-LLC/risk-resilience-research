# Urban farming infrastructure resilience analysis with synthetic data.

library(readr)
library(dplyr)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "raw", "urban_farming_resilience_synthetic.csv")
out_path <- file.path(root, "outputs", "tables", "urban_farming_resilience_summary_r.csv")
processed_path <- file.path(root, "data", "processed", "urban_farming_nodes_scored_r.csv")

df <- read_csv(data_path, show_col_types = FALSE) %>%
  mutate(
    yield_kg_per_m2 = annual_output_kg / land_area_m2,
    local_redundancy_ratio = annual_output_kg / essential_demand_kg,
    locally_distributed_output_kg = annual_output_kg * local_distribution_share,
    assumed_external_supply_kg = pmax(essential_demand_kg - annual_output_kg, 0),
    external_supply_lost_kg = assumed_external_supply_kg * shock_external_supply_loss_fraction,
    local_offset_share_of_shock_loss = if_else(
      external_supply_lost_kg > 0,
      annual_output_kg / external_supply_lost_kg,
      Inf
    ),
    water_use_total_liters = annual_output_kg * water_liters_per_kg,
    energy_use_total_kwh = annual_output_kg * energy_kwh_per_kg,
    waste_recapture_per_kg_output = waste_recapture_kg / annual_output_kg,
    high_priority_local_node = food_access_priority == "high" & local_distribution_share >= 0.75
  )

city_summary <- df %>%
  group_by(city) %>%
  summarise(
    nodes = n(),
    annual_output_kg = sum(annual_output_kg),
    essential_demand_kg = sum(essential_demand_kg),
    locally_distributed_output_kg = sum(locally_distributed_output_kg),
    land_area_m2 = sum(land_area_m2),
    waste_recapture_kg = sum(waste_recapture_kg),
    high_priority_nodes = sum(high_priority_local_node),
    city_redundancy_ratio = annual_output_kg / essential_demand_kg,
    yield_kg_per_m2 = annual_output_kg / land_area_m2,
    .groups = "drop"
  )

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(processed_path), recursive = TRUE, showWarnings = FALSE)

write_csv(df, processed_path)
write_csv(city_summary, out_path)

print(city_summary)
