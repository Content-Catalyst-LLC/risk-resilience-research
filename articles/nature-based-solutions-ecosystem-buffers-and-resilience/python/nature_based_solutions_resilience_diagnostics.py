"""
Advanced nature-based solutions, ecosystem buffers, and resilience diagnostics.

This workflow models:
- ecosystem condition
- biodiversity benefit
- ecological connectivity
- intervention quality
- governance capacity
- maintenance capacity
- hazard pressure
- exposure
- social vulnerability
- social legitimacy
- livelihood benefit
- displacement pressure
- nature-based-solution integrity
- hazard-vulnerability pressure
- buffer effectiveness
- nature-adjusted risk
- credibility risk
- justice-weighted nature-based risk
- nature-based resilience gaps
- scenario-based restoration, governance, and rights strategies
- Monte Carlo uncertainty around project classification

The sample data are illustrative. Replace them with documented ecological,
hazard, social vulnerability, land-cover, biodiversity, restoration, rights,
maintenance, and governance data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/nature-based-solutions-ecosystem-buffers-and-resilience")
DATA_FILE = BASE_DIR / "data" / "nature_based_solutions_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening nature-based resilience."""

    name: str
    ecosystem_condition_gain: float
    biodiversity_gain: float
    connectivity_gain: float
    intervention_quality_gain: float
    governance_gain: float
    maintenance_gain: float
    hazard_reduction: float
    exposure_reduction: float
    vulnerability_reduction: float
    legitimacy_gain: float
    livelihood_gain: float
    displacement_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "ecological_integrity": Scenario("ecological_integrity", .24, .30, .24, .20, .10, .12, .06, .04, .06, .08, .08, .06),
    "governance_and_maintenance": Scenario("governance_and_maintenance", .10, .10, .12, .18, .30, .30, .06, .08, .08, .18, .10, .12),
    "rights_and_social_legitimacy": Scenario("rights_and_social_legitimacy", .08, .10, .08, .14, .24, .16, .06, .12, .26, .34, .24, .34),
    "hazard_buffer_performance": Scenario("hazard_buffer_performance", .18, .18, .20, .24, .18, .18, .22, .20, .12, .14, .12, .12),
    "integrated_nature_based_resilience": Scenario("integrated_nature_based_resilience", .30, .32, .30, .30, .32, .32, .24, .24, .30, .34, .30, .34),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the nature-based-solution indicator panel."""
    df = pd.read_csv(path)

    required = {
        "project_id",
        "project_name",
        "region",
        "solution_type",
        "ecosystem_condition",
        "biodiversity_benefit",
        "ecological_connectivity",
        "intervention_quality",
        "governance_capacity",
        "maintenance_capacity",
        "hazard_pressure",
        "exposure",
        "social_vulnerability",
        "social_legitimacy",
        "livelihood_benefit",
        "displacement_pressure",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"project_id", "project_name", "region", "solution_type"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_projects(df: pd.DataFrame) -> pd.DataFrame:
    """Compute NBS integrity, effectiveness, credibility risk, and resilience-gap scores."""
    scored = df.copy()

    scored["nbs_integrity"] = (
        0.20 * scored["ecosystem_condition"]
        + 0.18 * scored["biodiversity_benefit"]
        + 0.16 * scored["ecological_connectivity"]
        + 0.16 * scored["intervention_quality"]
        + 0.15 * scored["governance_capacity"]
        + 0.15 * scored["maintenance_capacity"]
    )

    scored["hazard_vulnerability_pressure"] = (
        scored["hazard_pressure"]
        * scored["exposure"]
        * (1 + 0.35 * scored["social_vulnerability"])
    )

    scored["buffer_effectiveness"] = (
        scored["nbs_integrity"]
        * (1 + 0.22 * scored["social_legitimacy"])
        * (1 + 0.18 * scored["livelihood_benefit"])
    ).clip(0, 1.5)

    scored["nature_adjusted_risk"] = (
        scored["hazard_vulnerability_pressure"]
        * (1 - 0.45 * scored["buffer_effectiveness"].clip(0, 1))
        * (1 - 0.25 * scored["governance_capacity"])
    )

    scored["credibility_risk"] = (
        0.22 * (1 - scored["ecosystem_condition"])
        + 0.20 * (1 - scored["biodiversity_benefit"])
        + 0.18 * (1 - scored["social_legitimacy"])
        + 0.18 * (1 - scored["maintenance_capacity"])
        + 0.22 * scored["displacement_pressure"]
    )

    scored["justice_weighted_nbs_risk"] = (
        (scored["nature_adjusted_risk"] + scored["credibility_risk"])
        * (1 + 0.30 * scored["social_vulnerability"])
    )

    scored["nbs_resilience_gap"] = np.maximum(
        0,
        scored["justice_weighted_nbs_risk"] - scored["buffer_effectiveness"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["ecosystem_condition"] < 0.42,
            scored["biodiversity_benefit"] < 0.42,
            scored["social_legitimacy"] < 0.42,
            scored["maintenance_capacity"] < 0.42,
            scored["displacement_pressure"] > 0.62,
            scored["nbs_resilience_gap"] > 0.45,
        ],
        [
            "restore_ecological_condition",
            "strengthen_biodiversity_benefits",
            "repair_social_legitimacy_and_rights",
            "fund_long_term_maintenance",
            "reduce_displacement_and_green_gentrification_risk",
            "close_nature_based_resilience_gap",
        ],
        default="monitor_and_preserve_nbs_performance",
    )

    return scored.sort_values(
        ["nbs_resilience_gap", "justice_weighted_nbs_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a nature-based-solution scenario and rescore."""
    x = df.copy()

    x["ecosystem_condition"] += scenario.ecosystem_condition_gain
    x["biodiversity_benefit"] += scenario.biodiversity_gain
    x["ecological_connectivity"] += scenario.connectivity_gain
    x["intervention_quality"] += scenario.intervention_quality_gain
    x["governance_capacity"] += scenario.governance_gain
    x["maintenance_capacity"] += scenario.maintenance_gain
    x["hazard_pressure"] *= 1 - scenario.hazard_reduction
    x["exposure"] *= 1 - scenario.exposure_reduction
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["social_legitimacy"] += scenario.legitimacy_gain
    x["livelihood_benefit"] += scenario.livelihood_gain
    x["displacement_pressure"] *= 1 - scenario.displacement_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"project_id", "project_name", "region", "solution_type"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_projects(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all nature-based resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around NBS effectiveness, credibility risk, and resilience gaps."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"project_id", "project_name", "region", "solution_type"}
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
        scored = score_projects(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "project_id",
                    "project_name",
                    "draw",
                    "nbs_integrity",
                    "hazard_vulnerability_pressure",
                    "buffer_effectiveness",
                    "nature_adjusted_risk",
                    "credibility_risk",
                    "justice_weighted_nbs_risk",
                    "nbs_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["project_id", "project_name"])
        .agg(
            integrity_p50=("nbs_integrity", "median"),
            buffer_effectiveness_p50=("buffer_effectiveness", "median"),
            nature_adjusted_risk_p50=("nature_adjusted_risk", "median"),
            credibility_risk_p50=("credibility_risk", "median"),
            justice_risk_p50=("justice_weighted_nbs_risk", "median"),
            justice_risk_p95=("justice_weighted_nbs_risk", lambda x: np.quantile(x, .95)),
            resilience_gap_p50=("nbs_resilience_gap", "median"),
            resilience_gap_p95=("nbs_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full nature-based-solution resilience diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_projects(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            projects=("project_id", "count"),
            mean_integrity=("nbs_integrity", "mean"),
            mean_buffer_effectiveness=("buffer_effectiveness", "mean"),
            mean_nature_adjusted_risk=("nature_adjusted_risk", "mean"),
            mean_credibility_risk=("credibility_risk", "mean"),
            mean_resilience_gap=("nbs_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    type_summary = (
        scored.groupby("solution_type")
        .agg(
            projects=("project_id", "count"),
            mean_ecosystem_condition=("ecosystem_condition", "mean"),
            mean_biodiversity_benefit=("biodiversity_benefit", "mean"),
            mean_social_legitimacy=("social_legitimacy", "mean"),
            mean_buffer_effectiveness=("buffer_effectiveness", "mean"),
            mean_resilience_gap=("nbs_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "nature_based_solution_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "nature_based_solution_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "nature_based_solution_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "nature_based_solution_region_summary.csv", index=False)
    type_summary.to_csv(OUTPUT_DIR / "nature_based_solution_type_summary.csv", index=False)

    print("\nNature-based solution resilience diagnostics:")
    print(
        scored[
            [
                "project_name",
                "region",
                "solution_type",
                "nbs_integrity",
                "buffer_effectiveness",
                "nature_adjusted_risk",
                "credibility_risk",
                "justice_weighted_nbs_risk",
                "nbs_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
