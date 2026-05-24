# Desalination resilience analysis with synthetic data.
# Computes dependency ratios, outage supply, deficits, and storage coverage.

library(readr)
library(dplyr)

root <- normalizePath(file.path(dirname(sys.frame(1)$ofile), ".."))
data_path <- file.path(root, "data", "raw", "desalination_systems_synthetic.csv")
out_path <- file.path(root, "outputs", "tables", "desalination_resilience_summary_r.csv")
processed_path <- file.path(root, "data", "processed", "desalination_resilience_classified_r.csv")

df <- read_csv(data_path, show_col_types = FALSE) %>%
  mutate(
    normal_available_supply_mld =
      normal_desal_output_mld +
      alternative_supply_mld +
      emergency_transfer_mld -
      system_losses_mld,
    outage_desal_output_mld =
      (1 - outage_fraction) * normal_desal_output_mld,
    backup_power_adjusted_output_mld =
      normal_desal_output_mld * backup_power_fraction,
    outage_available_supply_mld =
      outage_desal_output_mld +
      alternative_supply_mld +
      emergency_transfer_mld -
      system_losses_mld,
    desalination_dependency_ratio =
      normal_desal_output_mld /
      (normal_desal_output_mld + alternative_supply_mld + emergency_transfer_mld),
    meets_priority_demand_under_outage =
      outage_available_supply_mld >= priority_demand_mld,
    daily_deficit_mld =
      pmax(priority_demand_mld - outage_available_supply_mld, 0),
    storage_coverage_days =
      if_else(daily_deficit_mld > 0, storage_reserve_mld / daily_deficit_mld, Inf),
    storage_covers_recovery_period =
      daily_deficit_mld == 0 | storage_coverage_days >= recovery_days
  )

summary <- df %>%
  select(
    city,
    plant,
    priority_demand_mld,
    normal_available_supply_mld,
    outage_available_supply_mld,
    desalination_dependency_ratio,
    daily_deficit_mld,
    storage_coverage_days,
    recovery_days,
    storage_covers_recovery_period,
    meets_priority_demand_under_outage
  )

dir.create(dirname(out_path), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(processed_path), recursive = TRUE, showWarnings = FALSE)

write_csv(df, processed_path)
write_csv(summary, out_path)

print(summary)
