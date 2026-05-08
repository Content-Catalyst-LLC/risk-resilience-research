"""
Advanced compound climate event and cascading social risk diagnostics.

This workflow models:
- concurrent hazard intensity
- sequential hazard pressure
- exposure
- social vulnerability
- infrastructure fragility
- health-system strain
- food-water-energy stress
- governance readiness
- cross-sector dependency
- recovery deficit
- inequality pressure
- ecological buffer condition
- social protection capacity
- communication reliability
- compound event severity
- cascade potential
- justice-weighted social risk
- continuity gaps
- scenario-based resilience strategies
- Monte Carlo uncertainty around risk classification

The sample data are illustrative. Replace them with documented climate hazard,
infrastructure, public-health, social vulnerability, ecosystem, and recovery data
before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/compound-climate-events-cascading-social-risk")
DATA_FILE = BASE_DIR / "data" / "compound_climate_social_risk_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    name: str
    concurrent_hazard_reduction: float
    sequential_hazard_reduction: float
    exposure_reduction: float
    vulnerability_reduction: float
    infrastructure_gain: float
    health_gain: float
    food_water_energy_gain: float
    governance_gain: float
    dependency_reduction: float
    recovery_gain: float
    inequality_reduction: float
    buffer_gain: float
    social_protection_gain: float
    communication_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "early_warning_and_communication": Scenario("early_warning_and_communication", .03, .04, .04, .08, .06, .08, .06, .16, .06, .08, .06, .06, .10, .28),
    "ecological_buffer_and_land_use": Scenario("ecological_buffer_and_land_use", .04, .08, .16, .08, .08, .06, .08, .10, .08, .10, .08, .30, .08, .10),
    "public_health_and_social_protection": Scenario("public_health_and_social_protection", .03, .05, .06, .24, .08, .28, .12, .16, .08, .16, .24, .08, .30, .14),
    "cross_sector_continuity": Scenario("cross_sector_continuity", .05, .10, .12, .14, .22, .18, .22, .26, .24, .22, .12, .16, .18, .20),
    "justice_centered_climate_resilience": Scenario("justice_centered_climate_resilience", .08, .14, .20, .28, .26, .26, .26, .30, .26, .28, .30, .30, .30, .28),
}


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "system_id",
        "system_name",
        "region",
        "event_type",
        "concurrent_hazard_intensity",
        "sequential_hazard_pressure",
        "exposure",
        "social_vulnerability",
        "infrastructure_fragility",
        "health_system_strain",
        "food_water_energy_stress",
        "governance_readiness",
        "cross_sector_dependency",
        "recovery_deficit",
        "inequality_pressure",
        "ecological_buffer_condition",
        "social_protection_capacity",
        "communication_reliability",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "event_type"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    s = df.copy()

    s["compound_event_severity"] = (
        0.42 * s["concurrent_hazard_intensity"]
        + 0.34 * s["sequential_hazard_pressure"]
        + 0.24 * s["exposure"]
    )

    s["social_sensitivity_index"] = (
        0.30 * s["social_vulnerability"]
        + 0.22 * s["health_system_strain"]
        + 0.20 * s["food_water_energy_stress"]
        + 0.16 * s["recovery_deficit"]
        + 0.12 * s["inequality_pressure"]
    )

    s["system_fragility_index"] = (
        0.30 * s["infrastructure_fragility"]
        + 0.28 * s["cross_sector_dependency"]
        + 0.18 * s["food_water_energy_stress"]
        + 0.14 * s["recovery_deficit"]
        + 0.10 * (1 - s["communication_reliability"])
    )

    s["resilience_capacity"] = (
        0.24 * s["governance_readiness"]
        + 0.22 * s["ecological_buffer_condition"]
        + 0.22 * s["social_protection_capacity"]
        + 0.18 * s["communication_reliability"]
        + 0.14 * (1 - s["recovery_deficit"])
    )

    s["cascade_potential"] = (
        s["compound_event_severity"]
        * (1 + 0.45 * s["system_fragility_index"])
        * (1 + 0.35 * s["cross_sector_dependency"])
        * (1 - 0.30 * s["resilience_capacity"])
    )

    s["justice_weighted_social_risk"] = (
        (
            0.38 * s["cascade_potential"]
            + 0.30 * s["social_sensitivity_index"]
            + 0.18 * s["recovery_deficit"]
            + 0.14 * s["inequality_pressure"]
        )
        * (1 + 0.35 * s["inequality_pressure"])
    )

    s["continuity_capacity"] = (
        0.28 * s["governance_readiness"]
        + 0.22 * s["social_protection_capacity"]
        + 0.20 * s["communication_reliability"]
        + 0.18 * s["ecological_buffer_condition"]
        + 0.12 * (1 - s["infrastructure_fragility"])
    )

    s["compound_resilience_gap"] = np.maximum(
        0,
        s["justice_weighted_social_risk"] - s["continuity_capacity"],
    )

    s["diagnostic_priority"] = np.select(
        [
            s["compound_event_severity"] > .76,
            s["cross_sector_dependency"] > .76,
            s["social_sensitivity_index"] > .72,
            s["governance_readiness"] < .45,
            s["ecological_buffer_condition"] < .40,
            s["compound_resilience_gap"] > .22,
        ],
        [
            "multi_hazard_preparedness",
            "cross_sector_dependency_mapping",
            "public_health_and_social_protection",
            "governance_and_warning_capacity",
            "restore_ecological_buffers",
            "close_compound_resilience_gap",
        ],
        default="monitor_and_strengthen_compound_resilience",
    )

    return s.sort_values(
        ["compound_resilience_gap", "justice_weighted_social_risk", "cascade_potential"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    x = df.copy()

    x["concurrent_hazard_intensity"] *= 1 - scenario.concurrent_hazard_reduction
    x["sequential_hazard_pressure"] *= 1 - scenario.sequential_hazard_reduction
    x["exposure"] *= 1 - scenario.exposure_reduction
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["infrastructure_fragility"] *= 1 - scenario.infrastructure_gain
    x["health_system_strain"] *= 1 - scenario.health_gain
    x["food_water_energy_stress"] *= 1 - scenario.food_water_energy_gain
    x["governance_readiness"] += scenario.governance_gain
    x["cross_sector_dependency"] *= 1 - scenario.dependency_reduction
    x["recovery_deficit"] *= 1 - scenario.recovery_gain
    x["inequality_pressure"] *= 1 - scenario.inequality_reduction
    x["ecological_buffer_condition"] += scenario.buffer_gain
    x["social_protection_capacity"] += scenario.social_protection_gain
    x["communication_reliability"] += scenario.communication_gain

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "event_type"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_systems(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([apply_scenario(df, s) for s in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "event_type"}
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
                    "compound_event_severity",
                    "social_sensitivity_index",
                    "system_fragility_index",
                    "cascade_potential",
                    "justice_weighted_social_risk",
                    "continuity_capacity",
                    "compound_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)
    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            compound_severity_p50=("compound_event_severity", "median"),
            cascade_p50=("cascade_potential", "median"),
            cascade_p95=("cascade_potential", lambda x: np.quantile(x, .95)),
            justice_risk_p50=("justice_weighted_social_risk", "median"),
            justice_risk_p95=("justice_weighted_social_risk", lambda x: np.quantile(x, .95)),
            continuity_p50=("continuity_capacity", "median"),
            resilience_gap_p50=("compound_resilience_gap", "median"),
            resilience_gap_p95=("compound_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_compound_event_severity=("compound_event_severity", "mean"),
            mean_cascade_potential=("cascade_potential", "mean"),
            mean_social_risk=("justice_weighted_social_risk", "mean"),
            mean_continuity_capacity=("continuity_capacity", "mean"),
            mean_resilience_gap=("compound_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    event_summary = (
        scored.groupby("event_type")
        .agg(
            systems=("system_id", "count"),
            mean_compound_event_severity=("compound_event_severity", "mean"),
            mean_system_fragility=("system_fragility_index", "mean"),
            mean_cascade_potential=("cascade_potential", "mean"),
            mean_resilience_gap=("compound_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "compound_climate_social_risk_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "compound_climate_social_risk_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "compound_climate_social_risk_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "compound_climate_social_risk_region_summary.csv", index=False)
    event_summary.to_csv(OUTPUT_DIR / "compound_climate_social_risk_event_summary.csv", index=False)

    print("\nCompound climate event and cascading social risk diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "event_type",
                "compound_event_severity",
                "cascade_potential",
                "justice_weighted_social_risk",
                "continuity_capacity",
                "compound_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
