"""
Advanced conflict, fragility, and resilience-under-stress diagnostics.

This workflow models:
- conflict intensity
- governance capacity
- service continuity
- institutional legitimacy
- administrative reach
- recovery capacity
- social vulnerability
- displacement pressure
- livelihood stress
- hazard exposure
- essential service demand
- inequality pressure
- institutional exclusion
- public trust
- repeated disruption pressure
- fragility pressure
- governance resilience
- conflict-amplified systemic risk
- service breakdown gaps
- legitimacy erosion
- resilience-under-stress gaps
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented conflict-event,
governance, service-continuity, displacement, livelihood, hazard, recovery,
public-trust, and institutional-capacity data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/conflict-fragility-and-resilience-under-stress")
DATA_FILE = BASE_DIR / "data" / "conflict_fragility_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening resilience under conflict and fragility."""

    name: str
    conflict_reduction: float
    governance_gain: float
    service_gain: float
    legitimacy_gain: float
    administrative_reach_gain: float
    recovery_gain: float
    vulnerability_reduction: float
    displacement_reduction: float
    livelihood_stress_reduction: float
    hazard_exposure_reduction: float
    service_demand_reduction: float
    inequality_reduction: float
    exclusion_reduction: float
    trust_gain: float
    repeated_disruption_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "service_continuity_and_protection": Scenario("service_continuity_and_protection", .08, .12, .30, .16, .14, .18, .12, .12, .10, .08, .20, .12, .12, .16, .12),
    "local_governance_and_legitimacy": Scenario("local_governance_and_legitimacy", .10, .26, .18, .32, .28, .18, .10, .10, .12, .06, .10, .20, .28, .34, .14),
    "displacement_and_livelihood_resilience": Scenario("displacement_and_livelihood_resilience", .08, .14, .16, .16, .16, .28, .18, .32, .34, .10, .18, .18, .16, .18, .22),
    "fragility_aware_early_warning": Scenario("fragility_aware_early_warning", .08, .20, .20, .18, .22, .22, .12, .12, .12, .24, .22, .14, .14, .20, .24),
    "integrated_resilience_under_stress": Scenario("integrated_resilience_under_stress", .24, .34, .34, .34, .34, .34, .30, .34, .32, .28, .30, .32, .32, .34, .30),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the conflict-fragility indicator panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "region",
        "fragility_context",
        "conflict_intensity",
        "governance_capacity",
        "service_continuity",
        "institutional_legitimacy",
        "administrative_reach",
        "recovery_capacity",
        "social_vulnerability",
        "displacement_pressure",
        "livelihood_stress",
        "hazard_exposure",
        "essential_service_demand",
        "inequality_pressure",
        "institutional_exclusion",
        "public_trust",
        "repeated_disruption_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "fragility_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute fragility, governance resilience, systemic risk, and resilience-gap scores."""
    scored = df.copy()

    scored["fragility_pressure"] = (
        0.24 * scored["conflict_intensity"]
        + 0.20 * scored["social_vulnerability"]
        + 0.18 * scored["displacement_pressure"]
        + 0.18 * scored["livelihood_stress"]
        + 0.20 * scored["hazard_exposure"]
    )

    scored["governance_resilience"] = (
        0.24 * scored["governance_capacity"]
        + 0.22 * scored["service_continuity"]
        + 0.20 * scored["institutional_legitimacy"]
        + 0.18 * scored["administrative_reach"]
        + 0.16 * scored["recovery_capacity"]
    )

    scored["conflict_amplified_systemic_risk"] = (
        scored["fragility_pressure"]
        * (1 + 0.45 * scored["conflict_intensity"])
        * (1 - 0.35 * scored["governance_resilience"])
    )

    scored["service_breakdown_gap"] = np.maximum(
        0,
        scored["essential_service_demand"] - scored["service_continuity"],
    )

    scored["legitimacy_erosion"] = (
        0.30 * scored["service_breakdown_gap"]
        + 0.26 * scored["inequality_pressure"]
        + 0.24 * scored["institutional_exclusion"]
        + 0.15 * scored["repeated_disruption_pressure"]
        - 0.20 * scored["public_trust"]
    ).clip(0, 1.5)

    scored["resilience_under_stress_gap"] = np.maximum(
        0,
        scored["conflict_amplified_systemic_risk"]
        + scored["service_breakdown_gap"]
        + scored["legitimacy_erosion"]
        - scored["governance_resilience"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["conflict_intensity"] > 0.72,
            scored["service_continuity"] < 0.42,
            scored["institutional_legitimacy"] < 0.42,
            scored["administrative_reach"] < 0.42,
            scored["displacement_pressure"] > 0.70,
            scored["resilience_under_stress_gap"] > 0.75,
        ],
        [
            "conflict_prevention_and_protection",
            "restore_essential_service_continuity",
            "repair_legitimacy_and_public_trust",
            "strengthen_administrative_reach",
            "protect_displaced_people_and_livelihoods",
            "close_resilience_under_stress_gap",
        ],
        default="monitor_and_strengthen_fragility_resilience",
    )

    return scored.sort_values(
        ["resilience_under_stress_gap", "conflict_amplified_systemic_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a resilience-under-stress scenario and rescore."""
    x = df.copy()

    x["conflict_intensity"] *= 1 - scenario.conflict_reduction
    x["governance_capacity"] += scenario.governance_gain
    x["service_continuity"] += scenario.service_gain
    x["institutional_legitimacy"] += scenario.legitimacy_gain
    x["administrative_reach"] += scenario.administrative_reach_gain
    x["recovery_capacity"] += scenario.recovery_gain
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["displacement_pressure"] *= 1 - scenario.displacement_reduction
    x["livelihood_stress"] *= 1 - scenario.livelihood_stress_reduction
    x["hazard_exposure"] *= 1 - scenario.hazard_exposure_reduction
    x["essential_service_demand"] *= 1 - scenario.service_demand_reduction
    x["inequality_pressure"] *= 1 - scenario.inequality_reduction
    x["institutional_exclusion"] *= 1 - scenario.exclusion_reduction
    x["public_trust"] += scenario.trust_gain
    x["repeated_disruption_pressure"] *= 1 - scenario.repeated_disruption_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "fragility_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_systems(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all conflict-fragility resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around conflict-fragility and governance resilience scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "fragility_context"}
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
                    "fragility_pressure",
                    "governance_resilience",
                    "conflict_amplified_systemic_risk",
                    "service_breakdown_gap",
                    "legitimacy_erosion",
                    "resilience_under_stress_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            fragility_pressure_p50=("fragility_pressure", "median"),
            governance_resilience_p50=("governance_resilience", "median"),
            systemic_risk_p50=("conflict_amplified_systemic_risk", "median"),
            systemic_risk_p95=("conflict_amplified_systemic_risk", lambda x: np.quantile(x, .95)),
            service_breakdown_p50=("service_breakdown_gap", "median"),
            legitimacy_erosion_p50=("legitimacy_erosion", "median"),
            resilience_gap_p50=("resilience_under_stress_gap", "median"),
            resilience_gap_p95=("resilience_under_stress_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full conflict-fragility and governance-resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_fragility_pressure=("fragility_pressure", "mean"),
            mean_governance_resilience=("governance_resilience", "mean"),
            mean_systemic_risk=("conflict_amplified_systemic_risk", "mean"),
            mean_service_gap=("service_breakdown_gap", "mean"),
            mean_resilience_gap=("resilience_under_stress_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    context_summary = (
        scored.groupby("fragility_context")
        .agg(
            systems=("system_id", "count"),
            mean_conflict_intensity=("conflict_intensity", "mean"),
            mean_service_continuity=("service_continuity", "mean"),
            mean_legitimacy=("institutional_legitimacy", "mean"),
            mean_fragility_pressure=("fragility_pressure", "mean"),
            mean_resilience_gap=("resilience_under_stress_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "conflict_fragility_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "conflict_fragility_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "conflict_fragility_resilience_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "conflict_fragility_region_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "conflict_fragility_context_summary.csv", index=False)

    print("\nConflict, fragility, and resilience-under-stress diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "fragility_context",
                "fragility_pressure",
                "governance_resilience",
                "conflict_amplified_systemic_risk",
                "service_breakdown_gap",
                "legitimacy_erosion",
                "resilience_under_stress_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
