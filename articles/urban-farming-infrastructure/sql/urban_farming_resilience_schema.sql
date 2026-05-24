-- Urban farming infrastructure resilience schema.
-- Synthetic data only.

DROP TABLE IF EXISTS urban_farming_nodes;

CREATE TABLE urban_farming_nodes (
    node_id TEXT PRIMARY KEY,
    city TEXT NOT NULL,
    neighborhood TEXT NOT NULL,
    production_type TEXT NOT NULL,
    crop_category TEXT NOT NULL,
    annual_output_kg REAL NOT NULL,
    served_households INTEGER NOT NULL,
    essential_demand_kg REAL NOT NULL,
    water_liters_per_kg REAL NOT NULL,
    energy_kwh_per_kg REAL NOT NULL,
    land_area_m2 REAL NOT NULL,
    food_access_priority TEXT NOT NULL,
    local_distribution_share REAL NOT NULL,
    waste_recapture_kg REAL NOT NULL,
    shock_external_supply_loss_fraction REAL NOT NULL
);

DROP VIEW IF EXISTS urban_farming_resilience_view;

CREATE VIEW urban_farming_resilience_view AS
SELECT
    node_id,
    city,
    neighborhood,
    production_type,
    crop_category,
    annual_output_kg,
    essential_demand_kg,
    annual_output_kg / NULLIF(essential_demand_kg, 0) AS local_redundancy_ratio,
    annual_output_kg / NULLIF(land_area_m2, 0) AS yield_kg_per_m2,
    annual_output_kg * local_distribution_share AS locally_distributed_output_kg,
    water_liters_per_kg,
    energy_kwh_per_kg,
    waste_recapture_kg / NULLIF(annual_output_kg, 0) AS waste_recapture_per_kg_output,
    CASE
      WHEN food_access_priority = 'high' AND local_distribution_share >= 0.75
      THEN 1 ELSE 0
    END AS high_priority_local_node
FROM urban_farming_nodes;
