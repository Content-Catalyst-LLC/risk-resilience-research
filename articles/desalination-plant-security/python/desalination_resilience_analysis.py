#!/usr/bin/env python3
"""
Desalination resilience analysis with synthetic data.

This script computes:
- normal available supply
- outage available supply
- desalination dependency ratio
- priority-demand service continuity
- daily deficit under outage
- storage coverage days
- backup-power-adjusted output
"""

from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "desalination_systems_synthetic.csv"
OUT = ROOT / "outputs" / "tables" / "desalination_resilience_summary.csv"
PROCESSED = ROOT / "data" / "processed" / "desalination_resilience_classified.csv"

def main() -> None:
    df = pd.read_csv(DATA)

    df["normal_available_supply_mld"] = (
        df["normal_desal_output_mld"]
        + df["alternative_supply_mld"]
        + df["emergency_transfer_mld"]
        - df["system_losses_mld"]
    )

    df["outage_desal_output_mld"] = (
        (1 - df["outage_fraction"]) * df["normal_desal_output_mld"]
    )

    df["backup_power_adjusted_output_mld"] = (
        df["normal_desal_output_mld"] * df["backup_power_fraction"]
    )

    df["outage_available_supply_mld"] = (
        df["outage_desal_output_mld"]
        + df["alternative_supply_mld"]
        + df["emergency_transfer_mld"]
        - df["system_losses_mld"]
    )

    df["desalination_dependency_ratio"] = (
        df["normal_desal_output_mld"]
        / (
            df["normal_desal_output_mld"]
            + df["alternative_supply_mld"]
            + df["emergency_transfer_mld"]
        )
    )

    df["meets_priority_demand_under_outage"] = (
        df["outage_available_supply_mld"] >= df["priority_demand_mld"]
    )

    df["daily_deficit_mld"] = np.maximum(
        df["priority_demand_mld"] - df["outage_available_supply_mld"],
        0
    )

    df["storage_coverage_days"] = np.where(
        df["daily_deficit_mld"] > 0,
        df["storage_reserve_mld"] / df["daily_deficit_mld"],
        np.inf
    )

    df["storage_covers_recovery_period"] = (
        (df["daily_deficit_mld"] == 0)
        | (df["storage_coverage_days"] >= df["recovery_days"])
    )

    summary_columns = [
        "city",
        "plant",
        "priority_demand_mld",
        "normal_available_supply_mld",
        "outage_available_supply_mld",
        "desalination_dependency_ratio",
        "daily_deficit_mld",
        "storage_coverage_days",
        "recovery_days",
        "storage_covers_recovery_period",
        "meets_priority_demand_under_outage",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED, index=False)
    df[summary_columns].to_csv(OUT, index=False)

    print("Desalination resilience summary written to:")
    print(OUT)
    print()
    print(df[summary_columns].to_string(index=False))

if __name__ == "__main__":
    main()
