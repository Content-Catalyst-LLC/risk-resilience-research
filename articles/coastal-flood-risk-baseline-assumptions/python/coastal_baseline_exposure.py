#!/usr/bin/env python3
"""
Coastal flood-risk baseline sensitivity analysis.

This script uses synthetic data to compare:
1. exposure under a modeled baseline assumption
2. exposure after adding a local baseline correction

The model is intentionally simplified for demonstration.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "coastal_assets_synthetic.csv"
OUT = ROOT / "outputs" / "tables" / "coastal_baseline_exposure_summary.csv"

def classify_exposure(df: pd.DataFrame, corrected: bool) -> pd.Series:
    baseline = df["modeled_baseline_m"]
    if corrected:
        baseline = baseline + df["baseline_correction_m"]

    water_height = (
        baseline
        + df["sea_level_rise_scenario_m"]
        + df["tide_surge_m"]
        + df["uncertainty_margin_m"]
    )

    exposure_threshold = df["land_elevation_m"] + df["protection_height_m"]
    return water_height >= exposure_threshold

def main() -> None:
    df = pd.read_csv(DATA)

    df["exposed_modeled_baseline"] = classify_exposure(df, corrected=False)
    df["exposed_corrected_baseline"] = classify_exposure(df, corrected=True)
    df["newly_exposed_after_correction"] = (
        ~df["exposed_modeled_baseline"] & df["exposed_corrected_baseline"]
    )

    summary = df.groupby("region", as_index=False).agg(
        sites=("site_id", "count"),
        population_total=("population", "sum"),
        population_exposed_modeled=("population", lambda s: s[df.loc[s.index, "exposed_modeled_baseline"]].sum()),
        population_exposed_corrected=("population", lambda s: s[df.loc[s.index, "exposed_corrected_baseline"]].sum()),
        asset_value_total_musd=("asset_value_musd", "sum"),
        asset_value_exposed_modeled_musd=("asset_value_musd", lambda s: s[df.loc[s.index, "exposed_modeled_baseline"]].sum()),
        asset_value_exposed_corrected_musd=("asset_value_musd", lambda s: s[df.loc[s.index, "exposed_corrected_baseline"]].sum()),
        newly_exposed_sites=("newly_exposed_after_correction", "sum"),
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ROOT / "data" / "processed" / "coastal_assets_exposure_classified.csv", index=False)
    summary.to_csv(OUT, index=False)

    print("Exposure summary written to:")
    print(OUT)
    print()
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
