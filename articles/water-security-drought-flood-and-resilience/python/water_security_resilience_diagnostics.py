"""
Advanced water security, drought, flood, and resilience diagnostics.

This workflow models:
- drought pressure
- flood exposure
- water demand pressure
- water availability
- infrastructure reliability
- water quality
- ecosystem buffer condition
- governance capacity
- social protection capacity
- livelihood water dependency
- critical service dependence
- inequality pressure
- recovery capacity
- maintenance deficits
- pollution pressure
- water security capacity
- hydrological risk pressure
- systemic water vulnerability
- justice-weighted water risk
- water-resilience gaps
- scenario-based resilience strategies
- Monte Carlo uncertainty around water-risk classification

The sample data are illustrative. Replace them with documented hydrological,
infrastructure, water quality, social vulnerability, ecological, governance,
and recovery data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/water-security-drought-flood-and-resilience")
DATA_FILE = BASE_DIR / "data" / "water_security_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening water security and hydrological resilience."""

    name: str
    drought_reduction: float
    flood_reduction: float
    demand_reduction: float
    availability_gain: float
    infrastructure_gain: float
    quality_gain: float
    ecosystem_gain: float
    governance_gain: float
    social_protection_gain: float
    livelihood_dependency_reduction: float
    critical_service_dependency_reduction: float
    inequality_reduction: float
    recovery_gain: float
    maintenance_reduction: float
    pollution_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "drought_demand_management": Scenario("drought_demand_management", .18, .02, .20, .10, .08, .06, .10, .14, .10, .10, .06, .08, .10, .10, .08),
    "flood_and_ecosystem_buffers": Scenario("flood_and_ecosystem_buffers", .06, .22, .06, .08, .14, .12, .30, .14, .10, .06, .08, .08, .12, .14, .12),
    "water_quality_and_public_health": Scenario("water_quality_and_public_health", .04, .08, .08, .08, .16, .30, .14, .18, .18, .08, .10, .14, .16, .18, .28),
    "justice_centered_water_security": Scenario("justice_centered_water_security", .16, .16, .18, .18, .22, .22, .20, .26, .30, .22, .20, .30, .28, .24, .22),
    "integrated_water_resilience": Scenario("integrated_water_resilience", .24, .24, .26, .24, .30, .30, .30, .30, .30, .26, .26, .28, .30, .30, .30),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the water-security indicator panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "region",
        "water_stress_type",
        "drought_pressure",
        "flood_exposure",
        "water_demand_pressure",
        "water_availability",
        "infrastructure_reliability",
        "water_quality",
        "ecosystem_buffer_condition",
        "governance_capacity",
        "social_protection_capacity",
        "livelihood_water_dependency",
        "critical_service_dependence",
        "inequality_pressure",
        "recovery_capacity",
        "maintenance_deficit",
        "pollution_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "water_stress_type"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute water-security, hydrological risk, vulnerability, and resilience-gap scores."""
    scored = df.copy()

    scored["water_stress_ratio"] = (
        scored["water_demand_pressure"] / (scored["water_availability"] + 0.05)
    ).clip(0, 2)

    scored["water_security_capacity"] = (
        0.20 * scored["water_availability"]
        + 0.18 * scored["infrastructure_reliability"]
        + 0.16 * scored["water_quality"]
        + 0.18 * scored["ecosystem_buffer_condition"]
        + 0.16 * scored["governance_capacity"]
        + 0.12 * scored["social_protection_capacity"]
    )

    scored["hydrological_risk_pressure"] = (
        0.24 * scored["drought_pressure"]
        + 0.24 * scored["flood_exposure"]
        + 0.18 * scored["water_stress_ratio"].clip(0, 1)
        + 0.18 * scored["pollution_pressure"]
        + 0.16 * scored["maintenance_deficit"]
    )

    scored["systemic_water_vulnerability"] = (
        0.24 * scored["livelihood_water_dependency"]
        + 0.20 * (1 - scored["recovery_capacity"])
        + 0.20 * scored["critical_service_dependence"]
        + 0.18 * (1 - scored["governance_capacity"])
        + 0.18 * scored["inequality_pressure"]
    )

    scored["justice_weighted_water_risk"] = (
        (scored["hydrological_risk_pressure"] + scored["systemic_water_vulnerability"])
        * (1 + 0.30 * scored["inequality_pressure"])
    )

    scored["water_resilience_gap"] = np.maximum(
        0,
        scored["justice_weighted_water_risk"] - scored["water_security_capacity"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["drought_pressure"] > 0.72,
            scored["flood_exposure"] > 0.72,
            scored["water_quality"] < 0.42,
            scored["ecosystem_buffer_condition"] < 0.40,
            scored["governance_capacity"] < 0.42,
            scored["water_resilience_gap"] > 0.55,
        ],
        [
            "drought_resilience_and_demand_management",
            "flood_risk_reduction_and_protection",
            "water_quality_and_public_health",
            "restore_ecological_water_buffers",
            "strengthen_water_governance",
            "close_water_resilience_gap",
        ],
        default="monitor_and_preserve_water_security",
    )

    return scored.sort_values(
        ["water_resilience_gap", "justice_weighted_water_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply water-resilience scenario assumptions and rescore."""
    x = df.copy()

    x["drought_pressure"] *= 1 - scenario.drought_reduction
    x["flood_exposure"] *= 1 - scenario.flood_reduction
    x["water_demand_pressure"] *= 1 - scenario.demand_reduction
    x["water_availability"] += scenario.availability_gain
    x["infrastructure_reliability"] += scenario.infrastructure_gain
    x["water_quality"] += scenario.quality_gain
    x["ecosystem_buffer_condition"] += scenario.ecosystem_gain
    x["governance_capacity"] += scenario.governance_gain
    x["social_protection_capacity"] += scenario.social_protection_gain
    x["livelihood_water_dependency"] *= 1 - scenario.livelihood_dependency_reduction
    x["critical_service_dependence"] *= 1 - scenario.critical_service_dependency_reduction
    x["inequality_pressure"] *= 1 - scenario.inequality_reduction
    x["recovery_capacity"] += scenario.recovery_gain
    x["maintenance_deficit"] *= 1 - scenario.maintenance_reduction
    x["pollution_pressure"] *= 1 - scenario.pollution_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "water_stress_type"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    rescored = score_systems(x)
    rescored["scenario"] = scenario.name
    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all water-resilience scenarios."""
    return pd.concat([apply_scenario(df, s) for s in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around water-risk and resilience-gap scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "water_stress_type"}
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
                    "water_stress_ratio",
                    "water_security_capacity",
                    "hydrological_risk_pressure",
                    "systemic_water_vulnerability",
                    "justice_weighted_water_risk",
                    "water_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)
    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            water_stress_p50=("water_stress_ratio", "median"),
            capacity_p50=("water_security_capacity", "median"),
            hydrological_risk_p50=("hydrological_risk_pressure", "median"),
            vulnerability_p50=("systemic_water_vulnerability", "median"),
            justice_risk_p50=("justice_weighted_water_risk", "median"),
            justice_risk_p95=("justice_weighted_water_risk", lambda x: np.quantile(x, .95)),
            resilience_gap_p50=("water_resilience_gap", "median"),
            resilience_gap_p95=("water_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full water-security and hydrological-resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_water_security_capacity=("water_security_capacity", "mean"),
            mean_hydrological_risk=("hydrological_risk_pressure", "mean"),
            mean_water_vulnerability=("systemic_water_vulnerability", "mean"),
            mean_justice_weighted_risk=("justice_weighted_water_risk", "mean"),
            mean_resilience_gap=("water_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    stress_summary = (
        scored.groupby("water_stress_type")
        .agg(
            systems=("system_id", "count"),
            mean_drought_pressure=("drought_pressure", "mean"),
            mean_flood_exposure=("flood_exposure", "mean"),
            mean_water_security_capacity=("water_security_capacity", "mean"),
            mean_hydrological_risk=("hydrological_risk_pressure", "mean"),
            mean_resilience_gap=("water_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "water_security_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "water_security_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "water_security_resilience_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "water_security_region_summary.csv", index=False)
    stress_summary.to_csv(OUTPUT_DIR / "water_security_stress_summary.csv", index=False)

    print("\nWater-security and hydrological-resilience diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "water_stress_type",
                "water_stress_ratio",
                "water_security_capacity",
                "hydrological_risk_pressure",
                "systemic_water_vulnerability",
                "justice_weighted_water_risk",
                "water_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
