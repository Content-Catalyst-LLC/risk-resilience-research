# Coastal flood-risk baseline sensitivity analysis in Julia.
# Synthetic demonstration only.

using CSV
using DataFrames

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "raw", "coastal_assets_synthetic.csv")
out_path = joinpath(root, "outputs", "tables", "coastal_baseline_exposure_summary_julia.csv")

df = CSV.read(data_path, DataFrame)

df.water_height_modeled =
    df.modeled_baseline_m .+
    df.sea_level_rise_scenario_m .+
    df.tide_surge_m .+
    df.uncertainty_margin_m

df.water_height_corrected =
    df.modeled_baseline_m .+
    df.baseline_correction_m .+
    df.sea_level_rise_scenario_m .+
    df.tide_surge_m .+
    df.uncertainty_margin_m

df.exposure_threshold =
    df.land_elevation_m .+ df.protection_height_m

df.exposed_modeled_baseline =
    df.water_height_modeled .>= df.exposure_threshold

df.exposed_corrected_baseline =
    df.water_height_corrected .>= df.exposure_threshold

mkpath(dirname(out_path))
CSV.write(out_path, df)

println(df[:, [
    :site_id,
    :region,
    :asset_type,
    :exposure_threshold,
    :water_height_modeled,
    :water_height_corrected,
    :exposed_modeled_baseline,
    :exposed_corrected_baseline
]])
