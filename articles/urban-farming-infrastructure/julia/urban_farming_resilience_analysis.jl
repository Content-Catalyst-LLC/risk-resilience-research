# Urban farming infrastructure resilience analysis in Julia.
# Synthetic demonstration only.

using CSV
using DataFrames

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "raw", "urban_farming_resilience_synthetic.csv")
out_path = joinpath(root, "outputs", "tables", "urban_farming_resilience_summary_julia.csv")

df = CSV.read(data_path, DataFrame)

df.yield_kg_per_m2 = df.annual_output_kg ./ df.land_area_m2
df.local_redundancy_ratio = df.annual_output_kg ./ df.essential_demand_kg
df.locally_distributed_output_kg = df.annual_output_kg .* df.local_distribution_share
df.water_use_total_liters = df.annual_output_kg .* df.water_liters_per_kg
df.energy_use_total_kwh = df.annual_output_kg .* df.energy_kwh_per_kg
df.waste_recapture_per_kg_output = df.waste_recapture_kg ./ df.annual_output_kg

mkpath(dirname(out_path))
CSV.write(out_path, df)

println(df[:, [
    :node_id,
    :city,
    :production_type,
    :yield_kg_per_m2,
    :local_redundancy_ratio,
    :locally_distributed_output_kg,
    :water_use_total_liters,
    :energy_use_total_kwh
]])
