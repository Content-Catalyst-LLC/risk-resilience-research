"""
Advanced migration, displacement, and resilience diagnostics.

This workflow models:
- hazard pressure
- livelihood stress
- conflict and insecurity pressure
- exposure
- social vulnerability
- adaptive capacity
- mobility resources
- protection access
- migration network strength
- destination service capacity
- host-community support
- recovery capacity
- arrival pressure
- mobility pressure
- adaptive mobility capacity
- forced-displacement risk
- trapped-population risk
- destination stress
- mobility resilience gaps
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented mobility,
displacement, climate, livelihood, conflict, service-capacity, remittance,
protection, recovery, and host-community data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/migration-displacement-and-resilience")
DATA_FILE = BASE_DIR / "data" / "migration_displacement_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening adaptive and protective mobility systems."""

    name: str
    hazard_reduction: float
    livelihood_stress_reduction: float
    conflict_reduction: float
    exposure_reduction: float
    vulnerability_reduction: float
    adaptive_capacity_gain: float
    mobility_resources_gain: float
    protection_access_gain: float
    network_gain: float
    destination_capacity_gain: float
    host_support_gain: float
    recovery_gain: float
    arrival_pressure_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "safe_mobility_and_protection": Scenario("safe_mobility_and_protection", .06, .08, .08, .08, .10, .14, .34, .34, .18, .14, .16, .18, .08),
    "origin_resilience_and_livelihoods": Scenario("origin_resilience_and_livelihoods", .18, .32, .10, .18, .22, .26, .18, .18, .16, .12, .14, .18, .06),
    "host_community_service_investment": Scenario("host_community_service_investment", .04, .06, .06, .06, .08, .14, .14, .16, .14, .34, .34, .28, .22),
    "trapped_population_protection": Scenario("trapped_population_protection", .10, .14, .08, .12, .28, .20, .30, .28, .24, .18, .18, .20, .08),
    "integrated_mobility_resilience": Scenario("integrated_mobility_resilience", .24, .34, .24, .28, .34, .34, .34, .34, .32, .34, .34, .34, .28),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the migration-displacement indicator panel."""
    df = pd.read_csv(path)

    required = {
        "place_id",
        "place_name",
        "region",
        "mobility_context",
        "hazard_pressure",
        "livelihood_stress",
        "conflict_insecurity_pressure",
        "exposure",
        "social_vulnerability",
        "adaptive_capacity",
        "mobility_resources",
        "protection_access",
        "migration_network_strength",
        "destination_service_capacity",
        "host_community_support",
        "recovery_capacity",
        "arrival_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"place_id", "place_name", "region", "mobility_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_places(df: pd.DataFrame) -> pd.DataFrame:
    """Compute mobility pressure, adaptive capacity, displacement risk, trapped-population risk, and gaps."""
    scored = df.copy()

    scored["mobility_pressure"] = (
        0.22 * scored["hazard_pressure"]
        + 0.20 * scored["livelihood_stress"]
        + 0.20 * scored["conflict_insecurity_pressure"]
        + 0.18 * scored["exposure"]
        + 0.20 * scored["social_vulnerability"]
    )

    scored["adaptive_mobility_capacity"] = (
        0.16 * scored["adaptive_capacity"]
        + 0.15 * scored["mobility_resources"]
        + 0.16 * scored["protection_access"]
        + 0.14 * scored["migration_network_strength"]
        + 0.14 * scored["destination_service_capacity"]
        + 0.13 * scored["host_community_support"]
        + 0.12 * scored["recovery_capacity"]
    )

    scored["forced_displacement_risk"] = (
        scored["mobility_pressure"]
        * (1 + 0.35 * scored["social_vulnerability"])
        * (1 - 0.45 * scored["adaptive_mobility_capacity"])
    )

    scored["trapped_population_risk"] = np.maximum(
        0,
        scored["mobility_pressure"]
        - scored["mobility_resources"]
        - scored["protection_access"]
        - scored["migration_network_strength"],
    )

    scored["destination_stress"] = (
        scored["arrival_pressure"]
        / (
            0.35
            + scored["destination_service_capacity"]
            + scored["host_community_support"]
            + scored["recovery_capacity"]
        )
    ).clip(0, 1.5)

    scored["mobility_resilience_gap"] = np.maximum(
        0,
        scored["forced_displacement_risk"]
        + scored["trapped_population_risk"]
        + scored["destination_stress"]
        - scored["adaptive_mobility_capacity"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["protection_access"] < 0.42,
            scored["mobility_resources"] < 0.42,
            scored["destination_service_capacity"] < 0.42,
            scored["host_community_support"] < 0.42,
            scored["trapped_population_risk"] > 0.25,
            scored["mobility_resilience_gap"] > 0.55,
        ],
        [
            "strengthen_rights_and_protection_access",
            "expand_safe_mobility_resources",
            "invest_in_destination_services",
            "support_host_communities",
            "protect_trapped_populations",
            "close_mobility_resilience_gap",
        ],
        default="monitor_and_strengthen_adaptive_mobility",
    )

    return scored.sort_values(
        ["mobility_resilience_gap", "forced_displacement_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a mobility-resilience scenario and rescore."""
    x = df.copy()

    x["hazard_pressure"] *= 1 - scenario.hazard_reduction
    x["livelihood_stress"] *= 1 - scenario.livelihood_stress_reduction
    x["conflict_insecurity_pressure"] *= 1 - scenario.conflict_reduction
    x["exposure"] *= 1 - scenario.exposure_reduction
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["adaptive_capacity"] += scenario.adaptive_capacity_gain
    x["mobility_resources"] += scenario.mobility_resources_gain
    x["protection_access"] += scenario.protection_access_gain
    x["migration_network_strength"] += scenario.network_gain
    x["destination_service_capacity"] += scenario.destination_capacity_gain
    x["host_community_support"] += scenario.host_support_gain
    x["recovery_capacity"] += scenario.recovery_gain
    x["arrival_pressure"] *= 1 - scenario.arrival_pressure_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"place_id", "place_name", "region", "mobility_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_places(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all mobility resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around mobility-pressure and resilience-gap scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"place_id", "place_name", "region", "mobility_context"}
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
        scored = score_places(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "place_id",
                    "place_name",
                    "draw",
                    "mobility_pressure",
                    "adaptive_mobility_capacity",
                    "forced_displacement_risk",
                    "trapped_population_risk",
                    "destination_stress",
                    "mobility_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["place_id", "place_name"])
        .agg(
            mobility_pressure_p50=("mobility_pressure", "median"),
            adaptive_capacity_p50=("adaptive_mobility_capacity", "median"),
            forced_displacement_p50=("forced_displacement_risk", "median"),
            forced_displacement_p95=("forced_displacement_risk", lambda x: np.quantile(x, .95)),
            trapped_population_p50=("trapped_population_risk", "median"),
            destination_stress_p50=("destination_stress", "median"),
            resilience_gap_p50=("mobility_resilience_gap", "median"),
            resilience_gap_p95=("mobility_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full migration, displacement, and resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_places(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            places=("place_id", "count"),
            mean_mobility_pressure=("mobility_pressure", "mean"),
            mean_adaptive_capacity=("adaptive_mobility_capacity", "mean"),
            mean_forced_displacement_risk=("forced_displacement_risk", "mean"),
            mean_trapped_population_risk=("trapped_population_risk", "mean"),
            mean_destination_stress=("destination_stress", "mean"),
            mean_resilience_gap=("mobility_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    context_summary = (
        scored.groupby("mobility_context")
        .agg(
            places=("place_id", "count"),
            mean_hazard_pressure=("hazard_pressure", "mean"),
            mean_livelihood_stress=("livelihood_stress", "mean"),
            mean_conflict_pressure=("conflict_insecurity_pressure", "mean"),
            mean_adaptive_capacity=("adaptive_mobility_capacity", "mean"),
            mean_resilience_gap=("mobility_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "migration_displacement_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "migration_displacement_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "migration_displacement_resilience_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "migration_displacement_region_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "migration_displacement_context_summary.csv", index=False)

    print("\nMigration, displacement, and resilience diagnostics:")
    print(
        scored[
            [
                "place_name",
                "region",
                "mobility_context",
                "mobility_pressure",
                "adaptive_mobility_capacity",
                "forced_displacement_risk",
                "trapped_population_risk",
                "destination_stress",
                "mobility_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
