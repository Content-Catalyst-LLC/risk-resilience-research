"""
Advanced community resilience, trust, and local-capacity diagnostics.

This workflow models:
- hazard pressure
- exposure
- social vulnerability
- trust level
- local organizational capacity
- mutual aid strength
- communication access
- local knowledge integration
- institutional support
- participation quality
- recovery capacity
- exclusion pressure
- institutional follow-through
- broken-promise pressure
- community hazard pressure
- local resilience capacity
- trust-adjusted response capacity
- participation legitimacy
- community resilience gaps
- updated trust projections
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented community
surveys, participatory mapping, public-service records, local-organization
inventories, trust measures, emergency response data, recovery outcomes, and
community-led planning data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/community-resilience-trust-and-local-capacity")
DATA_FILE = BASE_DIR / "data" / "community_resilience_trust_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening community resilience and trust."""

    name: str
    hazard_reduction: float
    exposure_reduction: float
    vulnerability_reduction: float
    trust_gain: float
    organizational_gain: float
    mutual_aid_gain: float
    communication_gain: float
    knowledge_integration_gain: float
    institutional_support_gain: float
    participation_gain: float
    recovery_gain: float
    exclusion_reduction: float
    follow_through_gain: float
    broken_promise_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "trust_and_accountability": Scenario("trust_and_accountability", .04, .06, .08, .34, .12, .12, .16, .14, .24, .24, .14, .28, .34, .34),
    "local_organization_and_mutual_aid": Scenario("local_organization_and_mutual_aid", .04, .08, .10, .16, .34, .34, .20, .18, .18, .18, .16, .16, .18, .18),
    "communication_and_local_knowledge": Scenario("communication_and_local_knowledge", .06, .10, .12, .18, .18, .16, .34, .34, .18, .20, .16, .18, .18, .18),
    "participation_and_shared_authority": Scenario("participation_and_shared_authority", .06, .10, .14, .22, .20, .18, .18, .22, .32, .34, .20, .34, .30, .28),
    "integrated_community_resilience": Scenario("integrated_community_resilience", .18, .24, .30, .34, .34, .34, .34, .34, .34, .34, .32, .34, .34, .34),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the community resilience indicator panel."""
    df = pd.read_csv(path)

    required = {
        "community_id",
        "community_name",
        "region",
        "risk_context",
        "hazard_pressure",
        "exposure",
        "social_vulnerability",
        "trust_level",
        "local_organizational_capacity",
        "mutual_aid_strength",
        "communication_access",
        "local_knowledge_integration",
        "institutional_support",
        "participation_quality",
        "recovery_capacity",
        "exclusion_pressure",
        "institutional_follow_through",
        "broken_promise_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"community_id", "community_name", "region", "risk_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_communities(df: pd.DataFrame) -> pd.DataFrame:
    """Compute local capacity, response capacity, participation, trust, and gaps."""
    scored = df.copy()

    scored["community_hazard_pressure"] = (
        scored["hazard_pressure"]
        * scored["exposure"]
        * (1 + 0.40 * scored["social_vulnerability"])
    )

    scored["local_resilience_capacity"] = (
        0.16 * scored["trust_level"]
        + 0.15 * scored["local_organizational_capacity"]
        + 0.14 * scored["mutual_aid_strength"]
        + 0.13 * scored["communication_access"]
        + 0.14 * scored["local_knowledge_integration"]
        + 0.12 * scored["institutional_support"]
        + 0.08 * scored["participation_quality"]
        + 0.08 * scored["recovery_capacity"]
    )

    scored["trust_adjusted_response_capacity"] = (
        (
            0.28 * scored["local_organizational_capacity"]
            + 0.25 * scored["mutual_aid_strength"]
            + 0.24 * scored["communication_access"]
            + 0.23 * scored["local_knowledge_integration"]
        )
        * (1 + 0.35 * scored["trust_level"])
    ).clip(0, 1.5)

    scored["participation_legitimacy"] = (
        scored["participation_quality"]
        * (1 + 0.25 * scored["institutional_support"])
        * (1 - 0.35 * scored["exclusion_pressure"])
    ).clip(0, 1.5)

    scored["community_resilience_gap"] = np.maximum(
        0,
        scored["community_hazard_pressure"]
        - scored["trust_adjusted_response_capacity"]
        - scored["participation_legitimacy"],
    )

    scored["updated_trust_projection"] = (
        scored["trust_level"]
        + 0.30 * scored["institutional_follow_through"]
        - 0.35 * scored["broken_promise_pressure"]
        - 0.20 * scored["exclusion_pressure"]
    ).clip(0, 1)

    scored["diagnostic_priority"] = np.select(
        [
            scored["trust_level"] < 0.42,
            scored["local_organizational_capacity"] < 0.42,
            scored["communication_access"] < 0.42,
            scored["local_knowledge_integration"] < 0.42,
            scored["participation_quality"] < 0.42,
            scored["community_resilience_gap"] > 0.35,
        ],
        [
            "repair_trust_and_public_accountability",
            "resource_local_organizations",
            "strengthen_accessible_communication",
            "integrate_local_and_scientific_knowledge",
            "improve_participation_and_shared_authority",
            "close_community_resilience_gap",
        ],
        default="monitor_and_strengthen_local_capacity",
    )

    return scored.sort_values(
        ["community_resilience_gap", "community_hazard_pressure"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a community resilience scenario and rescore."""
    x = df.copy()

    x["hazard_pressure"] *= 1 - scenario.hazard_reduction
    x["exposure"] *= 1 - scenario.exposure_reduction
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["trust_level"] += scenario.trust_gain
    x["local_organizational_capacity"] += scenario.organizational_gain
    x["mutual_aid_strength"] += scenario.mutual_aid_gain
    x["communication_access"] += scenario.communication_gain
    x["local_knowledge_integration"] += scenario.knowledge_integration_gain
    x["institutional_support"] += scenario.institutional_support_gain
    x["participation_quality"] += scenario.participation_gain
    x["recovery_capacity"] += scenario.recovery_gain
    x["exclusion_pressure"] *= 1 - scenario.exclusion_reduction
    x["institutional_follow_through"] += scenario.follow_through_gain
    x["broken_promise_pressure"] *= 1 - scenario.broken_promise_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"community_id", "community_name", "region", "risk_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_communities(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all community resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around local capacity, trust, and resilience gaps."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"community_id", "community_name", "region", "risk_context"}
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
        scored = score_communities(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "community_id",
                    "community_name",
                    "draw",
                    "community_hazard_pressure",
                    "local_resilience_capacity",
                    "trust_adjusted_response_capacity",
                    "participation_legitimacy",
                    "community_resilience_gap",
                    "updated_trust_projection",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["community_id", "community_name"])
        .agg(
            hazard_pressure_p50=("community_hazard_pressure", "median"),
            local_capacity_p50=("local_resilience_capacity", "median"),
            response_capacity_p50=("trust_adjusted_response_capacity", "median"),
            participation_legitimacy_p50=("participation_legitimacy", "median"),
            resilience_gap_p50=("community_resilience_gap", "median"),
            resilience_gap_p95=("community_resilience_gap", lambda x: np.quantile(x, .95)),
            trust_projection_p50=("updated_trust_projection", "median"),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full community resilience and trust diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_communities(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            communities=("community_id", "count"),
            mean_hazard_pressure=("community_hazard_pressure", "mean"),
            mean_local_capacity=("local_resilience_capacity", "mean"),
            mean_response_capacity=("trust_adjusted_response_capacity", "mean"),
            mean_participation_legitimacy=("participation_legitimacy", "mean"),
            mean_resilience_gap=("community_resilience_gap", "mean"),
            mean_updated_trust=("updated_trust_projection", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    context_summary = (
        scored.groupby("risk_context")
        .agg(
            communities=("community_id", "count"),
            mean_hazard_pressure=("hazard_pressure", "mean"),
            mean_trust=("trust_level", "mean"),
            mean_local_capacity=("local_resilience_capacity", "mean"),
            mean_participation_quality=("participation_quality", "mean"),
            mean_resilience_gap=("community_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "community_resilience_trust_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "community_resilience_trust_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "community_resilience_trust_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "community_resilience_region_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "community_resilience_context_summary.csv", index=False)

    print("\nCommunity resilience, trust, and local-capacity diagnostics:")
    print(
        scored[
            [
                "community_name",
                "region",
                "risk_context",
                "community_hazard_pressure",
                "local_resilience_capacity",
                "trust_adjusted_response_capacity",
                "participation_legitimacy",
                "community_resilience_gap",
                "updated_trust_projection",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
