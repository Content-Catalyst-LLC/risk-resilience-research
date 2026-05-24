-- Desalination plant security and water-resilience schema.
-- Synthetic data only. Not for operational use.

DROP TABLE IF EXISTS desalination_systems;

CREATE TABLE desalination_systems (
    city TEXT NOT NULL,
    region TEXT NOT NULL,
    plant TEXT PRIMARY KEY,
    served_population INTEGER NOT NULL,
    priority_demand_mld REAL NOT NULL,
    normal_desal_output_mld REAL NOT NULL,
    alternative_supply_mld REAL NOT NULL,
    storage_reserve_mld REAL NOT NULL,
    emergency_transfer_mld REAL NOT NULL,
    system_losses_mld REAL NOT NULL,
    outage_fraction REAL NOT NULL,
    backup_power_fraction REAL NOT NULL,
    recovery_days REAL NOT NULL
);

DROP VIEW IF EXISTS desalination_resilience_view;

CREATE VIEW desalination_resilience_view AS
SELECT
    city,
    region,
    plant,
    priority_demand_mld,
    normal_desal_output_mld
      + alternative_supply_mld
      + emergency_transfer_mld
      - system_losses_mld AS normal_available_supply_mld,
    ((1 - outage_fraction) * normal_desal_output_mld)
      + alternative_supply_mld
      + emergency_transfer_mld
      - system_losses_mld AS outage_available_supply_mld,
    normal_desal_output_mld
      / NULLIF(normal_desal_output_mld + alternative_supply_mld + emergency_transfer_mld, 0)
      AS desalination_dependency_ratio,
    CASE
      WHEN (((1 - outage_fraction) * normal_desal_output_mld)
        + alternative_supply_mld
        + emergency_transfer_mld
        - system_losses_mld) >= priority_demand_mld
      THEN 1 ELSE 0
    END AS meets_priority_demand_under_outage
FROM desalination_systems;
