"""
Advanced public health resilience and systemic-risk diagnostics.

This workflow models:
- health hazard pressure
- exposure
- social and health vulnerability
- surveillance capacity
- prevention capacity
- essential service continuity
- workforce capacity
- supply-chain reliability
- public trust
- communication capacity
- recovery capacity
- inequality pressure
- essential service demand
- repeated health disruption pressure
- public health threat pressure
- public health resilience capacity
- systemic health risk
- continuity gaps
- trust-adjusted response capacity
- public health resilience gaps
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented surveillance,
laboratory, service continuity, workforce, supply-chain, social vulnerability,
health-equity, emergency response, climate-health, and public-trust data before
applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/public-health-resilience-and-systemic-risk")
DATA_FILE = BASE_DIR / "data" / "public_health_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening public health resilience."""

    name: str
    hazard_reduction: float
    exposure_reduction: float
    vulnerability_reduction: float
    surveillance_gain: float
    prevention_gain: float
    continuity_gain: float
    workforce_gain: float
    supply_chain_gain: float
    trust_gain: float
    communication_gain: float
    recovery_gain: float
    inequality_reduction: float
    service_demand_reduction: float
    repeated_disruption_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "surveillance_and_laboratory_strengthening": Scenario("surveillance_and_laboratory_strengthening", .06, .06, .08, .32, .16, .12, .12, .14, .10, .18, .10, .08, .08, .10),
    "essential_service_continuity": Scenario("essential_service_continuity", .06, .08, .10, .14, .18, .34, .22, .20, .12, .14, .26, .12, .28, .18),
    "workforce_and_supply_chain_resilience": Scenario("workforce_and_supply_chain_resilience", .04, .06, .08, .14, .14, .20, .34, .34, .10, .10, .20, .10, .18, .18),
    "trust_communication_and_equity": Scenario("trust_communication_and_equity", .06, .10, .28, .16, .20, .16, .16, .12, .34, .34, .18, .32, .18, .18),
    "integrated_public_health_resilience": Scenario("integrated_public_health_resilience", .18, .24, .30, .34, .32, .34, .34, .34, .34, .34, .32, .34, .32, .30),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the public-health resilience indicator panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "region",
        "health_risk_context",
        "health_hazard_pressure",
        "exposure",
        "social_health_vulnerability",
        "surveillance_capacity",
        "prevention_capacity",
        "essential_service_continuity",
        "workforce_capacity",
        "supply_chain_reliability",
        "public_trust",
        "communication_capacity",
        "recovery_capacity",
        "inequality_pressure",
        "essential_service_demand",
        "repeated_health_disruption_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "health_risk_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute threat pressure, resilience capacity, systemic risk, and gaps."""
    scored = df.copy()

    scored["public_health_threat_pressure"] = (
        scored["health_hazard_pressure"]
        * scored["exposure"]
        * (1 + 0.40 * scored["social_health_vulnerability"])
    )

    scored["public_health_resilience_capacity"] = (
        0.16 * scored["surveillance_capacity"]
        + 0.14 * scored["prevention_capacity"]
        + 0.16 * scored["essential_service_continuity"]
        + 0.14 * scored["workforce_capacity"]
        + 0.12 * scored["supply_chain_reliability"]
        + 0.12 * scored["public_trust"]
        + 0.08 * scored["communication_capacity"]
        + 0.08 * scored["recovery_capacity"]
    )

    scored["systemic_health_risk"] = (
        scored["public_health_threat_pressure"]
        * (1 - 0.45 * scored["public_health_resilience_capacity"])
        * (1 + 0.35 * scored["inequality_pressure"])
        * (1 + 0.15 * scored["repeated_health_disruption_pressure"])
    )

    scored["continuity_gap"] = np.maximum(
        0,
        scored["essential_service_demand"] - scored["essential_service_continuity"],
    )

    scored["trust_adjusted_response_capacity"] = (
        (
            0.34 * scored["surveillance_capacity"]
            + 0.33 * scored["communication_capacity"]
            + 0.33 * scored["prevention_capacity"]
        )
        * (1 + 0.30 * scored["public_trust"])
    ).clip(0, 1.5)

    scored["public_health_resilience_gap"] = np.maximum(
        0,
        scored["systemic_health_risk"]
        + scored["continuity_gap"]
        - scored["trust_adjusted_response_capacity"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["surveillance_capacity"] < 0.42,
            scored["essential_service_continuity"] < 0.42,
            scored["workforce_capacity"] < 0.42,
            scored["supply_chain_reliability"] < 0.42,
            scored["public_trust"] < 0.42,
            scored["public_health_resilience_gap"] > 0.55,
        ],
        [
            "strengthen_surveillance_and_laboratories",
            "protect_essential_service_continuity",
            "rebuild_workforce_capacity",
            "stabilize_health_supply_chains",
            "repair_trust_and_risk_communication",
            "close_public_health_resilience_gap",
        ],
        default="monitor_and_strengthen_public_health_resilience",
    )

    return scored.sort_values(
        ["public_health_resilience_gap", "systemic_health_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a public-health resilience scenario and rescore."""
    x = df.copy()

    x["health_hazard_pressure"] *= 1 - scenario.hazard_reduction
    x["exposure"] *= 1 - scenario.exposure_reduction
    x["social_health_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["surveillance_capacity"] += scenario.surveillance_gain
    x["prevention_capacity"] += scenario.prevention_gain
    x["essential_service_continuity"] += scenario.continuity_gain
    x["workforce_capacity"] += scenario.workforce_gain
    x["supply_chain_reliability"] += scenario.supply_chain_gain
    x["public_trust"] += scenario.trust_gain
    x["communication_capacity"] += scenario.communication_gain
    x["recovery_capacity"] += scenario.recovery_gain
    x["inequality_pressure"] *= 1 - scenario.inequality_reduction
    x["essential_service_demand"] *= 1 - scenario.service_demand_reduction
    x["repeated_health_disruption_pressure"] *= 1 - scenario.repeated_disruption_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "health_risk_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_systems(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all public-health resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around public-health risk and resilience scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "health_risk_context"}
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
                    "public_health_threat_pressure",
                    "public_health_resilience_capacity",
                    "systemic_health_risk",
                    "continuity_gap",
                    "trust_adjusted_response_capacity",
                    "public_health_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            threat_pressure_p50=("public_health_threat_pressure", "median"),
            resilience_capacity_p50=("public_health_resilience_capacity", "median"),
            systemic_health_risk_p50=("systemic_health_risk", "median"),
            systemic_health_risk_p95=("systemic_health_risk", lambda x: np.quantile(x, .95)),
            continuity_gap_p50=("continuity_gap", "median"),
            response_capacity_p50=("trust_adjusted_response_capacity", "median"),
            resilience_gap_p50=("public_health_resilience_gap", "median"),
            resilience_gap_p95=("public_health_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full public-health resilience and systemic-risk workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_threat_pressure=("public_health_threat_pressure", "mean"),
            mean_resilience_capacity=("public_health_resilience_capacity", "mean"),
            mean_systemic_health_risk=("systemic_health_risk", "mean"),
            mean_continuity_gap=("continuity_gap", "mean"),
            mean_resilience_gap=("public_health_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    context_summary = (
        scored.groupby("health_risk_context")
        .agg(
            systems=("system_id", "count"),
            mean_hazard_pressure=("health_hazard_pressure", "mean"),
            mean_vulnerability=("social_health_vulnerability", "mean"),
            mean_resilience_capacity=("public_health_resilience_capacity", "mean"),
            mean_systemic_health_risk=("systemic_health_risk", "mean"),
            mean_resilience_gap=("public_health_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "public_health_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "public_health_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "public_health_resilience_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "public_health_region_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "public_health_context_summary.csv", index=False)

    print("\nPublic health resilience and systemic-risk diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "health_risk_context",
                "public_health_threat_pressure",
                "public_health_resilience_capacity",
                "systemic_health_risk",
                "continuity_gap",
                "trust_adjusted_response_capacity",
                "public_health_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
