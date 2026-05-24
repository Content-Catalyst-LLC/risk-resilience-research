-- Coastal flood-risk baseline sensitivity schema.
-- Synthetic data only.

DROP TABLE IF EXISTS coastal_assets;

CREATE TABLE coastal_assets (
    site_id TEXT PRIMARY KEY,
    region TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    population INTEGER NOT NULL,
    asset_value_musd REAL NOT NULL,
    land_elevation_m REAL NOT NULL,
    protection_height_m REAL NOT NULL,
    modeled_baseline_m REAL NOT NULL,
    baseline_correction_m REAL NOT NULL,
    sea_level_rise_scenario_m REAL NOT NULL,
    tide_surge_m REAL NOT NULL,
    uncertainty_margin_m REAL NOT NULL
);

DROP VIEW IF EXISTS coastal_exposure_thresholds;

CREATE VIEW coastal_exposure_thresholds AS
SELECT
    site_id,
    region,
    asset_type,
    population,
    asset_value_musd,
    land_elevation_m + protection_height_m AS exposure_threshold_m,
    modeled_baseline_m
      + sea_level_rise_scenario_m
      + tide_surge_m
      + uncertainty_margin_m AS water_height_modeled_m,
    modeled_baseline_m
      + baseline_correction_m
      + sea_level_rise_scenario_m
      + tide_surge_m
      + uncertainty_margin_m AS water_height_corrected_m,
    CASE
      WHEN modeled_baseline_m
        + sea_level_rise_scenario_m
        + tide_surge_m
        + uncertainty_margin_m
        >= land_elevation_m + protection_height_m
      THEN 1 ELSE 0
    END AS exposed_modeled_baseline,
    CASE
      WHEN modeled_baseline_m
        + baseline_correction_m
        + sea_level_rise_scenario_m
        + tide_surge_m
        + uncertainty_margin_m
        >= land_elevation_m + protection_height_m
      THEN 1 ELSE 0
    END AS exposed_corrected_baseline
FROM coastal_assets;
