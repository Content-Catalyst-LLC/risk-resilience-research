"""
Advanced ecosystem resilience and natural-buffer diagnostics.

This workflow models:
- ecosystem condition
- ecological connectivity
- functional biodiversity
- maintenance capacity
- restoration investment
- hazard pressure
- exposure
- social vulnerability
- governance capacity
- degradation pressure
- natural-buffer capacity
- hazard-exposure pressure
- buffer-adjusted risk
- ecological fragility
- justice-weighted ecosystem risk
- ecosystem-resilience gaps
- scenario-based restoration and governance strategies
- Monte Carlo uncertainty around ecosystem-risk classification

The sample data are illustrative. Replace them with documented ecological,
hazard, social vulnerability, land-cover, biodiversity, restoration, and
governance data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/ecosystem-resilience-and-natural-buffers")
DATA_FILE = BASE_DIR / "data" / "ecosystem_buffer_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening ecosystem resilience."""

    name: str
    condition_gain: float
    connectivity_gain: float
    biodiversity_gain: float
    maintenance_gain: float
    restoration_gain: float
    hazard_reduction: float
    exposure_reduction: float
    vulnerability_reduction: float
    governance_gain: float
    degradation_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "ecosystem_restoration": Scenario("ecosystem_restoration", .22, .16, .18, .16, .30, .06, .06, .08, .12, .24),
    "connectivity_and_biodiversity": Scenario("connectivity_and_biodiversity", .14, .30, .30, .12, .18, .04, .04, .06, .12, .18),
    "governance_and_maintenance": Scenario("governance_and_maintenance", .12, .12, .10, .30, .20, .06, .08, .10, .30, .20),
    "justice_centered_buffer_protection": Scenario("justice_centered_buffer_protection", .18, .18, .16, .22, .24, .10, .18, .28, .26, .24),
    "integrated_ecosystem_resilience": Scenario("integrated_ecosystem_resilience", .30, .30, .30, .30, .34, .18, .22, .30, .30, .30),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the ecosystem-buffer indicator panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "region",
        "ecosystem_type",
        "ecosystem_condition",
        "ecological_connectivity",
        "functional_biodiversity",
        "maintenance_capacity",
        "restoration_investment",
        "hazard_pressure",
        "exposure",
        "social_vulnerability",
        "governance_capacity",
        "degradation_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "ecosystem_type"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute natural-buffer capacity, risk, fragility, and resilience-gap scores."""
    scored = df.copy()

    scored["natural_buffer_capacity"] = (
        0.24 * scored["ecosystem_condition"]
        + 0.20 * scored["ecological_connectivity"]
        + 0.20 * scored["functional_biodiversity"]
        + 0.18 * scored["maintenance_capacity"]
        + 0.18 * scored["restoration_investment"]
    )

    scored["hazard_exposure_pressure"] = (
        scored["hazard_pressure"]
        * scored["exposure"]
        * (1 + 0.35 * scored["social_vulnerability"])
    )

    scored["buffer_adjusted_risk"] = (
        scored["hazard_exposure_pressure"]
        * (1 - 0.45 * scored["natural_buffer_capacity"])
        * (1 - 0.25 * scored["governance_capacity"])
    )

    scored["ecological_fragility"] = (
        0.28 * (1 - scored["ecosystem_condition"])
        + 0.24 * (1 - scored["ecological_connectivity"])
        + 0.22 * (1 - scored["functional_biodiversity"])
        + 0.14 * (1 - scored["maintenance_capacity"])
        + 0.12 * scored["degradation_pressure"]
    )

    scored["justice_weighted_ecosystem_risk"] = (
        (scored["buffer_adjusted_risk"] + scored["ecological_fragility"])
        * (1 + 0.30 * scored["social_vulnerability"])
    )

    scored["ecosystem_resilience_gap"] = np.maximum(
        0,
        scored["justice_weighted_ecosystem_risk"] - scored["natural_buffer_capacity"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["ecosystem_condition"] < 0.40,
            scored["ecological_connectivity"] < 0.40,
            scored["functional_biodiversity"] < 0.40,
            scored["hazard_pressure"] > 0.74,
            scored["governance_capacity"] < 0.42,
            scored["ecosystem_resilience_gap"] > 0.55,
        ],
        [
            "restore_ecosystem_condition",
            "reconnect_habitats_and_buffers",
            "protect_functional_biodiversity",
            "reduce_exposure_to_hazard_pressure",
            "strengthen_ecological_governance",
            "close_ecosystem_resilience_gap",
        ],
        default="monitor_and_preserve_natural_buffers",
    )

    return scored.sort_values(
        ["ecosystem_resilience_gap", "justice_weighted_ecosystem_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply an ecosystem-resilience scenario and rescore."""
    x = df.copy()

    x["ecosystem_condition"] += scenario.condition_gain
    x["ecological_connectivity"] += scenario.connectivity_gain
    x["functional_biodiversity"] += scenario.biodiversity_gain
    x["maintenance_capacity"] += scenario.maintenance_gain
    x["restoration_investment"] += scenario.restoration_gain
    x["hazard_pressure"] *= 1 - scenario.hazard_reduction
    x["exposure"] *= 1 - scenario.exposure_reduction
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["governance_capacity"] += scenario.governance_gain
    x["degradation_pressure"] *= 1 - scenario.degradation_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "ecosystem_type"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    rescored = score_systems(x)
    rescored["scenario"] = scenario.name
    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all ecosystem-resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around natural-buffer and ecosystem-resilience scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "ecosystem_type"}
    ]

    frames = []
    for draw in range(draws):
        sample = df.copy()
        sample[numeric_cols] = np.clip(
            sample[numeric_cols].to_numpy()
            + rng.normal(0, 0.04, size=(len(sample), len(numeric_cols))),
            0,
            1,
        )
        scored = score_systems(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "system_id",
                    "system_name",
                    "draw",
                    "natural_buffer_capacity",
                    "hazard_exposure_pressure",
                    "buffer_adjusted_risk",
                    "ecological_fragility",
                    "justice_weighted_ecosystem_risk",
                    "ecosystem_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            buffer_capacity_p50=("natural_buffer_capacity", "median"),
            hazard_pressure_p50=("hazard_exposure_pressure", "median"),
            buffer_adjusted_risk_p50=("buffer_adjusted_risk", "median"),
            ecological_fragility_p50=("ecological_fragility", "median"),
            justice_risk_p50=("justice_weighted_ecosystem_risk", "median"),
            justice_risk_p95=("justice_weighted_ecosystem_risk", lambda x: np.quantile(x, .95)),
            resilience_gap_p50=("ecosystem_resilience_gap", "median"),
            resilience_gap_p95=("ecosystem_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full ecosystem-buffer and natural-resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_buffer_capacity=("natural_buffer_capacity", "mean"),
            mean_buffer_adjusted_risk=("buffer_adjusted_risk", "mean"),
            mean_ecological_fragility=("ecological_fragility", "mean"),
            mean_resilience_gap=("ecosystem_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    type_summary = (
        scored.groupby("ecosystem_type")
        .agg(
            systems=("system_id", "count"),
            mean_ecosystem_condition=("ecosystem_condition", "mean"),
            mean_connectivity=("ecological_connectivity", "mean"),
            mean_biodiversity=("functional_biodiversity", "mean"),
            mean_buffer_capacity=("natural_buffer_capacity", "mean"),
            mean_resilience_gap=("ecosystem_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "ecosystem_buffer_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "ecosystem_buffer_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "ecosystem_buffer_resilience_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "ecosystem_buffer_region_summary.csv", index=False)
    type_summary.to_csv(OUTPUT_DIR / "ecosystem_buffer_type_summary.csv", index=False)

    print("\nEcosystem resilience and natural-buffer diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "ecosystem_type",
                "natural_buffer_capacity",
                "hazard_exposure_pressure",
                "buffer_adjusted_risk",
                "ecological_fragility",
                "justice_weighted_ecosystem_risk",
                "ecosystem_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
