# Coastal flood-risk baseline sensitivity analysis
# Uses synthetic data to compare modeled-baseline and corrected-baseline exposure.

library(readr)
library(dplyr)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "raw", "coastal_assets_synthetic.csv")
out_path <- file.path(root, "outputs", "tables", "coastal_baseline_exposure_summary_r.csv")
processed_path <- file.path(root, "data", "processed", "coastal_assets_exposure_classified_r.csv")

df <- read_csv(data_path, show_col_types = FALSE) %>%
  mutate(
    water_height_modeled =
      modeled_baseline_m +
      sea_level_rise_scenario_m +
      tide_surge_m +
      uncertainty_margin_m,
    water_height_corrected =
      modeled_baseline_m +
      baseline_correction_m +
      sea_level_rise_scenario_m +
      tide_surge_m +
      uncertainty_margin_m,
    exposure_threshold =
      land_elevation_m + protection_height_m,
    exposed_modeled_baseline =
      water_height_modeled >= exposure_threshold,
    exposed_corrected_baseline =
      water_height_corrected >= exposure_threshold,
    newly_exposed_after_correction =
      !exposed_modeled_baseline & exposed_corrected_baseline
  )

summary <- df %>%
  group_by(region) %>%
  summarise(
    sites = n(),
    population_total = sum(population),
    population_exposed_modeled = sum(population[exposed_modeled_baseline]),
    population_exposed_corrected = sum(population[exposed_corrected_baseline]),
    asset_value_total_musd = sum(asset_value_musd),
    asset_value_exposed_modeled_musd = sum(asset_value_musd[exposed_modeled_baseline]),
    asset_value_exposed_corrected_musd = sum(asset_value_musd[exposed_corrected_baseline]),
    newly_exposed_sites = sum(newly_exposed_after_correction),
    .groups = "drop"
  )

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(processed_path), recursive = TRUE, showWarnings = FALSE)

write_csv(df, processed_path)
write_csv(summary, out_path)

print(summary)
