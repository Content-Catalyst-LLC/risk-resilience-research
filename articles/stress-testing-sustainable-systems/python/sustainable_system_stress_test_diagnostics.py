"""
Advanced stress testing diagnostics for sustainable systems.

This workflow models:
- baseline capacity
- hazard or stress intensity
- exposure
- social vulnerability
- interdependence exposure
- redundancy
- recovery capacity
- governance capacity
- monitoring maturity
- threshold level
- stress load
- resilience capacity
- failure pressure
- threshold proximity
- service-continuity gaps
- stress-test priority scoring
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented climate projections,
disaster-risk models, infrastructure condition data, public-service capacity data,
social vulnerability indicators, budget data, supply-chain records, cyber dependency
maps, and recovery-time measurements before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/stress-testing-sustainable-systems")
DATA_FILE = BASE_DIR / "data" / "sustainable_system_stress_test_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for sustainable-system stress testing."""

    name: str
    hazard_intensity_increase: float
    exposure_increase: float
    vulnerability_increase: float
    interdependence_increase: float
    redundancy_gain: float
    recovery_gain: float
    governance_gain: float
    monitoring_gain: float
    threshold_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "moderate_compound_stress": Scenario("moderate_compound_stress", .10, .08, .08, .08, 0, 0, 0, 0, 0),
    "severe_compound_stress": Scenario("severe_compound_stress", .22, .18, .16, .18, 0, 0, 0, 0, 0),
    "redundancy_and_recovery_investment": Scenario("redundancy_and_recovery_investment", .10, .08, .06, .08, .28, .32, .14, .16, .10),
    "governance_monitoring_and_early_warning": Scenario("governance_monitoring_and_early_warning", .10, .08, .06, .08, .12, .18, .34, .34, .12),
    "integrated_resilience_upgrade": Scenario("integrated_resilience_upgrade", .16, .14, .12, .14, .34, .34, .34, .34, .24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the sustainable-system stress-test panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "sector",
        "stress_context",
        "baseline_capacity",
        "hazard_intensity",
        "exposure",
        "social_vulnerability",
        "interdependence_exposure",
        "redundancy",
        "recovery_capacity",
        "governance_capacity",
        "monitoring_maturity",
        "threshold_level",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "sector", "stress_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_stress_tests(df: pd.DataFrame) -> pd.DataFrame:
    """Compute stress load, resilience capacity, threshold proximity, and priority."""
    scored = df.copy()

    scored["stress_load"] = (
        scored["hazard_intensity"]
        * scored["exposure"]
        * (1 + 0.35 * scored["social_vulnerability"])
        * (1 + 0.30 * scored["interdependence_exposure"])
    )

    scored["resilience_capacity"] = (
        0.24 * scored["baseline_capacity"]
        + 0.20 * scored["redundancy"]
        + 0.20 * scored["recovery_capacity"]
        + 0.18 * scored["governance_capacity"]
        + 0.18 * scored["monitoring_maturity"]
    )

    scored["failure_pressure"] = (
        scored["stress_load"]
        * (1 - 0.45 * scored["resilience_capacity"])
    )

    scored["threshold_proximity"] = (
        scored["stress_load"]
        / (0.20 + scored["threshold_level"] + scored["resilience_capacity"])
    ).clip(0, 1.5)

    scored["service_continuity_gap"] = np.maximum(
        0,
        scored["stress_load"] - scored["resilience_capacity"],
    )

    scored["stress_test_priority_score"] = (
        scored["service_continuity_gap"]
        + 0.35 * scored["threshold_proximity"]
        + 0.25 * scored["social_vulnerability"]
        + 0.25 * scored["interdependence_exposure"]
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["threshold_proximity"] > 0.75,
            scored["service_continuity_gap"] > 0.35,
            scored["redundancy"] < 0.40,
            scored["recovery_capacity"] < 0.40,
            scored["governance_capacity"] < 0.40,
            scored["monitoring_maturity"] < 0.40,
        ],
        [
            "reduce_threshold_proximity",
            "close_service_continuity_gap",
            "increase_redundancy_and_buffers",
            "strengthen_recovery_capacity",
            "strengthen_governance_and_coordination",
            "improve_monitoring_and_early_warning",
        ],
        default="monitor_and_retest_under_updated_scenarios",
    )

    return scored.sort_values(
        ["stress_test_priority_score", "threshold_proximity"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a stress or resilience-upgrade scenario and rescore."""
    x = df.copy()

    x["hazard_intensity"] += scenario.hazard_intensity_increase
    x["exposure"] += scenario.exposure_increase
    x["social_vulnerability"] += scenario.vulnerability_increase
    x["interdependence_exposure"] += scenario.interdependence_increase
    x["redundancy"] += scenario.redundancy_gain
    x["recovery_capacity"] += scenario.recovery_gain
    x["governance_capacity"] += scenario.governance_gain
    x["monitoring_maturity"] += scenario.monitoring_gain
    x["threshold_level"] += scenario.threshold_gain

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "sector", "stress_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_stress_tests(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all stress-test and resilience-upgrade scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around threshold proximity and stress-test priority scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "sector", "stress_context"}
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
        scored = score_stress_tests(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "system_id",
                    "system_name",
                    "draw",
                    "stress_load",
                    "resilience_capacity",
                    "failure_pressure",
                    "threshold_proximity",
                    "service_continuity_gap",
                    "stress_test_priority_score",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            stress_load_p50=("stress_load", "median"),
            resilience_capacity_p50=("resilience_capacity", "median"),
            failure_pressure_p50=("failure_pressure", "median"),
            threshold_proximity_p50=("threshold_proximity", "median"),
            threshold_proximity_p95=("threshold_proximity", lambda x: np.quantile(x, .95)),
            continuity_gap_p50=("service_continuity_gap", "median"),
            priority_p50=("stress_test_priority_score", "median"),
            priority_p95=("stress_test_priority_score", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("priority_p50", ascending=False)
    )


def main() -> None:
    """Run the full sustainable-system stress testing workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_stress_tests(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    sector_summary = (
        scored.groupby("sector")
        .agg(
            systems=("system_id", "count"),
            mean_stress_load=("stress_load", "mean"),
            mean_resilience_capacity=("resilience_capacity", "mean"),
            mean_failure_pressure=("failure_pressure", "mean"),
            mean_threshold_proximity=("threshold_proximity", "mean"),
            mean_continuity_gap=("service_continuity_gap", "mean"),
            mean_priority=("stress_test_priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_priority", ascending=False)
    )

    context_summary = (
        scored.groupby("stress_context")
        .agg(
            systems=("system_id", "count"),
            mean_hazard_intensity=("hazard_intensity", "mean"),
            mean_exposure=("exposure", "mean"),
            mean_vulnerability=("social_vulnerability", "mean"),
            mean_interdependence=("interdependence_exposure", "mean"),
            mean_threshold_proximity=("threshold_proximity", "mean"),
        )
        .reset_index()
        .sort_values("mean_threshold_proximity", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "sustainable_system_stress_test_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "sustainable_system_stress_test_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "sustainable_system_stress_test_uncertainty.csv", index=False)
    sector_summary.to_csv(OUTPUT_DIR / "sustainable_system_stress_test_sector_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "sustainable_system_stress_test_context_summary.csv", index=False)

    print("\nSustainable-system stress testing diagnostics:")
    print(
        scored[
            [
                "system_name",
                "sector",
                "stress_context",
                "stress_load",
                "resilience_capacity",
                "failure_pressure",
                "threshold_proximity",
                "service_continuity_gap",
                "stress_test_priority_score",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
