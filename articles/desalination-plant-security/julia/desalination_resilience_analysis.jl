# Desalination resilience analysis in Julia.
# Synthetic demonstration only.

using CSV
using DataFrames

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "raw", "desalination_systems_synthetic.csv")
out_path = joinpath(root, "outputs", "tables", "desalination_resilience_summary_julia.csv")

df = CSV.read(data_path, DataFrame)

df.normal_available_supply_mld =
    df.normal_desal_output_mld .+
    df.alternative_supply_mld .+
    df.emergency_transfer_mld .-
    df.system_losses_mld

df.outage_desal_output_mld =
    (1 .- df.outage_fraction) .* df.normal_desal_output_mld

df.outage_available_supply_mld =
    df.outage_desal_output_mld .+
    df.alternative_supply_mld .+
    df.emergency_transfer_mld .-
    df.system_losses_mld

df.desalination_dependency_ratio =
    df.normal_desal_output_mld ./ (
        df.normal_desal_output_mld .+
        df.alternative_supply_mld .+
        df.emergency_transfer_mld
    )

df.meets_priority_demand_under_outage =
    df.outage_available_supply_mld .>= df.priority_demand_mld

df.daily_deficit_mld =
    max.(df.priority_demand_mld .- df.outage_available_supply_mld, 0)

df.storage_coverage_days =
    ifelse.(df.daily_deficit_mld .> 0, df.storage_reserve_mld ./ df.daily_deficit_mld, Inf)

df.storage_covers_recovery_period =
    (df.daily_deficit_mld .== 0) .| (df.storage_coverage_days .>= df.recovery_days)

mkpath(dirname(out_path))
CSV.write(out_path, df)

println(df[:, [
    :city,
    :plant,
    :priority_demand_mld,
    :outage_available_supply_mld,
    :desalination_dependency_ratio,
    :daily_deficit_mld,
    :storage_coverage_days,
    :storage_covers_recovery_period
]])
