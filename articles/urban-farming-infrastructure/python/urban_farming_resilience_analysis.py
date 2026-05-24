#!/usr/bin/env python3
"""
Urban farming infrastructure resilience analysis with synthetic data.

This script computes:
- yield per square meter
- local redundancy ratio
- locally distributed output
- external supply lost in a shock scenario
- partial local offset from urban production
- water, energy, and circularity indicators
"""

from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "urban_farming_resilience_synthetic.csv"
OUT = ROOT / "outputs" / "tables" / "urban_farming_resilience_summary.csv"
PROCESSED = ROOT / "data" / "processed" / "urban_farming_nodes_scored.csv"

def main() -> None:
    df = pd.read_csv(DATA)

    df["yield_kg_per_m2"] = df["annual_output_kg"] / df["land_area_m2"]
    df["local_redundancy_ratio"] = df["annual_output_kg"] / df["essential_demand_kg"]
    df["locally_distributed_output_kg"] = df["annual_output_kg"] * df["local_distribution_share"]

    df["assumed_external_supply_kg"] = df["essential_demand_kg"] - df["annual_output_kg"]
    df["assumed_external_supply_kg"] = df["assumed_external_supply_kg"].clip(lower=0)

    df["external_supply_lost_kg"] = (
        df["assumed_external_supply_kg"] * df["shock_external_supply_loss_fraction"]
    )

    df["local_offset_share_of_shock_loss"] = np.where(
        df["external_supply_lost_kg"] > 0,
        df["annual_output_kg"] / df["external_supply_lost_kg"],
        np.inf
    )

    df["water_use_total_liters"] = df["annual_output_kg"] * df["water_liters_per_kg"]
    df["energy_use_total_kwh"] = df["annual_output_kg"] * df["energy_kwh_per_kg"]
    df["waste_recapture_per_kg_output"] = df["waste_recapture_kg"] / df["annual_output_kg"]

    df["high_priority_local_node"] = (
        (df["food_access_priority"] == "high")
        & (df["local_distribution_share"] >= 0.75)
    )

    city_summary = df.groupby("city", as_index=False).agg(
        nodes=("node_id", "count"),
        annual_output_kg=("annual_output_kg", "sum"),
        essential_demand_kg=("essential_demand_kg", "sum"),
        locally_distributed_output_kg=("locally_distributed_output_kg", "sum"),
        land_area_m2=("land_area_m2", "sum"),
        waste_recapture_kg=("waste_recapture_kg", "sum"),
        high_priority_nodes=("high_priority_local_node", "sum"),
    )

    city_summary["city_redundancy_ratio"] = (
        city_summary["annual_output_kg"] / city_summary["essential_demand_kg"]
    )
    city_summary["yield_kg_per_m2"] = (
        city_summary["annual_output_kg"] / city_summary["land_area_m2"]
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED, index=False)
    city_summary.to_csv(OUT, index=False)

    print("Urban farming resilience summary written to:")
    print(OUT)
    print()
    print(city_summary.to_string(index=False))

if __name__ == "__main__":
    main()
