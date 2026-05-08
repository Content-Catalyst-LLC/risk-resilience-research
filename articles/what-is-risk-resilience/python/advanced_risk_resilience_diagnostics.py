"""
Advanced risk and resilience diagnostics for sustainable systems.

This workflow goes beyond the article-level explanation by modeling:
- hazard, exposure, vulnerability, and capacity
- cascading systemic risk
- resilience capacity and resilience gaps
- justice-sensitive vulnerability
- transformation readiness
- scenario-based resilience improvement
- Monte Carlo uncertainty around system risk

The sample data are illustrative. Replace them with documented hazard,
infrastructure, social, ecological, and governance indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/what-is-risk-resilience")
DATA_FILE = BASE_DIR / "data" / "risk_resilience_system_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for resilience intervention modeling."""

    name: str
    hazard_reduction: float
    vulnerability_reduction: float
    adaptive_capacity_gain: float
    governance_capacity_gain: float
    ecological_buffer_gain: float
    redundancy_gain: float
    early_warning_gain: float
    transformation_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario(
        name="baseline",
        hazard_reduction=0.00,
        vulnerability_reduction=0.00,
        adaptive_capacity_gain=0.00,
        governance_capacity_gain=0.00,
        ecological_buffer_gain=0.00,
        redundancy_gain=0.00,
        early_warning_gain=0.00,
        transformation_gain=0.00,
    ),
    "preparedness_upgrade": Scenario(
        name="preparedness_upgrade",
        hazard_reduction=0.02,
        vulnerability_reduction=0.05,
        adaptive_capacity_gain=0.10,
        governance_capacity_gain=0.08,
        ecological_buffer_gain=0.04,
        redundancy_gain=0.08,
        early_warning_gain=0.18,
        transformation_gain=0.05,
    ),
    "ecological_buffer_restoration": Scenario(
        name="ecological_buffer_restoration",
        hazard_reduction=0.08,
        vulnerability_reduction=0.08,
        adaptive_capacity_gain=0.07,
        governance_capacity_gain=0.06,
        ecological_buffer_gain=0.24,
        redundancy_gain=0.06,
        early_warning_gain=0.06,
        transformation_gain=0.08,
    ),
    "justice_centered_adaptation": Scenario(
        name="justice_centered_adaptation",
        hazard_reduction=0.04,
        vulnerability_reduction=0.18,
        adaptive_capacity_gain=0.14,
        governance_capacity_gain=0.14,
        ecological_buffer_gain=0.10,
        redundancy_gain=0.10,
        early_warning_gain=0.12,
        transformation_gain=0.16,
    ),
    "deep_resilience_transformation": Scenario(
        name="deep_resilience_transformation",
        hazard_reduction=0.10,
        vulnerability_reduction=0.22,
        adaptive_capacity_gain=0.22,
        governance_capacity_gain=0.20,
        ecological_buffer_gain=0.22,
        redundancy_gain=0.18,
        early_warning_gain=0.18,
        transformation_gain=0.26,
    ),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load the system panel and validate expected columns."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "hazard_type",
        "hazard_intensity",
        "exposure_index",
        "social_vulnerability",
        "infrastructure_vulnerability",
        "ecological_vulnerability",
        "adaptive_capacity",
        "governance_capacity",
        "ecological_buffer_capacity",
        "redundancy_index",
        "early_warning_capacity",
        "transformation_capacity",
        "supply_chain_dependency",
        "critical_infrastructure_dependency",
        "social_inequality_index",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [col for col in df.columns if col not in {
        "system_id",
        "system_name",
        "domain",
        "region",
        "hazard_type",
    }]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def classify_band(value: float, low: float, high: float) -> str:
    """Classify a normalized value into lower, moderate, or elevated bands."""
    if value < low:
        return "lower"
    if value < high:
        return "moderate"
    return "elevated"


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute advanced risk and resilience diagnostics."""
    scored = df.copy()

    # Risk is relational: hazard becomes dangerous through exposure and vulnerability.
    scored["hazard_exposure_load"] = (
        scored["hazard_intensity"] * scored["exposure_index"]
    )

    scored["composite_vulnerability"] = (
        0.42 * scored["social_vulnerability"]
        + 0.32 * scored["infrastructure_vulnerability"]
        + 0.26 * scored["ecological_vulnerability"]
    )

    # Capacity is deliberately plural: no single capacity dimension is enough.
    scored["composite_capacity"] = (
        0.24 * scored["adaptive_capacity"]
        + 0.22 * scored["governance_capacity"]
        + 0.22 * scored["ecological_buffer_capacity"]
        + 0.14 * scored["redundancy_index"]
        + 0.10 * scored["early_warning_capacity"]
        + 0.08 * scored["transformation_capacity"]
    )

    # Base risk increases with hazard/exposure and vulnerability, but falls with capacity.
    scored["base_risk"] = (
        scored["hazard_exposure_load"]
        * (1 + scored["composite_vulnerability"])
        * (1 - scored["composite_capacity"])
    )

    # Cascading risk captures system interdependence and the tendency of shocks to propagate.
    scored["cascade_multiplier"] = (
        1
        + 0.24 * scored["supply_chain_dependency"]
        + 0.24 * scored["critical_infrastructure_dependency"]
        + 0.22 * scored["social_inequality_index"]
        + 0.16 * scored["ecological_vulnerability"]
        + 0.14 * scored["infrastructure_vulnerability"]
    )

    scored["systemic_risk_score"] = (
        scored["base_risk"] * scored["cascade_multiplier"]
    )

    # Resilience is not merely recovery; transformation capacity matters.
    scored["resilience_capacity_score"] = (
        0.20 * scored["adaptive_capacity"]
        + 0.18 * scored["governance_capacity"]
        + 0.18 * scored["ecological_buffer_capacity"]
        + 0.14 * scored["redundancy_index"]
        + 0.12 * scored["early_warning_capacity"]
        + 0.18 * scored["transformation_capacity"]
    )

    scored["justice_adjusted_vulnerability"] = (
        scored["composite_vulnerability"]
        * (1 + 0.35 * scored["social_inequality_index"])
    )

    scored["resilience_gap"] = np.maximum(
        0,
        scored["systemic_risk_score"] - scored["resilience_capacity_score"],
    )

    scored["transformation_readiness"] = (
        0.35 * scored["transformation_capacity"]
        + 0.25 * scored["governance_capacity"]
        + 0.20 * scored["adaptive_capacity"]
        + 0.20 * scored["redundancy_index"]
    )

    scored["risk_band"] = scored["systemic_risk_score"].apply(
        lambda x: classify_band(x, low=0.25, high=0.55)
    )

    scored["resilience_band"] = scored["resilience_capacity_score"].apply(
        lambda x: classify_band(x, low=0.40, high=0.65)
    )

    scored["priority_class"] = np.select(
        [
            (scored["risk_band"] == "elevated") & (scored["resilience_band"] != "elevated"),
            (scored["justice_adjusted_vulnerability"] > 0.75),
            (scored["resilience_gap"] > 0.20),
            (scored["transformation_readiness"] > 0.65),
        ],
        [
            "urgent_risk_reduction",
            "justice_centered_adaptation",
            "capacity_building_priority",
            "transformation_leverage",
        ],
        default="monitor_and_maintain",
    )

    return scored.sort_values("systemic_risk_score", ascending=False).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply intervention scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["hazard_intensity"] = (
        scenario_df["hazard_intensity"] * (1 - scenario.hazard_reduction)
    ).clip(0, 1)

    for col in [
        "social_vulnerability",
        "infrastructure_vulnerability",
        "ecological_vulnerability",
    ]:
        scenario_df[col] = (
            scenario_df[col] * (1 - scenario.vulnerability_reduction)
        ).clip(0, 1)

    scenario_df["adaptive_capacity"] = (
        scenario_df["adaptive_capacity"] + scenario.adaptive_capacity_gain
    ).clip(0, 1)

    scenario_df["governance_capacity"] = (
        scenario_df["governance_capacity"] + scenario.governance_capacity_gain
    ).clip(0, 1)

    scenario_df["ecological_buffer_capacity"] = (
        scenario_df["ecological_buffer_capacity"] + scenario.ecological_buffer_gain
    ).clip(0, 1)

    scenario_df["redundancy_index"] = (
        scenario_df["redundancy_index"] + scenario.redundancy_gain
    ).clip(0, 1)

    scenario_df["early_warning_capacity"] = (
        scenario_df["early_warning_capacity"] + scenario.early_warning_gain
    ).clip(0, 1)

    scenario_df["transformation_capacity"] = (
        scenario_df["transformation_capacity"] + scenario.transformational_gain
        if hasattr(scenario, "transformational_gain")
        else scenario_df["transformation_capacity"] + scenario.transformation_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all resilience scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 5000,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Run Monte Carlo uncertainty around key indicators.

    This helps avoid false precision. Each numeric indicator is perturbed
    within a bounded uncertainty envelope, then the system is rescored.
    """
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "hazard_intensity",
        "exposure_index",
        "social_vulnerability",
        "infrastructure_vulnerability",
        "ecological_vulnerability",
        "adaptive_capacity",
        "governance_capacity",
        "ecological_buffer_capacity",
        "redundancy_index",
        "early_warning_capacity",
        "transformation_capacity",
        "supply_chain_dependency",
        "critical_infrastructure_dependency",
        "social_inequality_index",
    ]

    for draw in range(draws):
        sampled = df.copy()

        # Moderate uncertainty: perturb indicators with normally distributed error.
        noise = rng.normal(loc=0.0, scale=0.045, size=(len(df), len(numeric_cols)))
        sampled[numeric_cols] = np.clip(sampled[numeric_cols].to_numpy() + noise, 0, 1)

        scored = score_systems(sampled)
        scored["draw"] = draw
        records.append(
            scored[
                [
                    "system_id",
                    "system_name",
                    "draw",
                    "systemic_risk_score",
                    "resilience_capacity_score",
                    "resilience_gap",
                    "justice_adjusted_vulnerability",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    summary = (
        mc.groupby(["system_id", "system_name"])
        .agg(
            risk_p05=("systemic_risk_score", lambda x: np.quantile(x, 0.05)),
            risk_p50=("systemic_risk_score", "median"),
            risk_p95=("systemic_risk_score", lambda x: np.quantile(x, 0.95)),
            resilience_p50=("resilience_capacity_score", "median"),
            gap_p50=("resilience_gap", "median"),
            justice_vulnerability_p50=("justice_adjusted_vulnerability", "median"),
        )
        .reset_index()
        .sort_values("risk_p50", ascending=False)
    )

    return summary


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize risk and resilience by sustainable-system domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_systemic_risk=("systemic_risk_score", "mean"),
            mean_resilience_capacity=("resilience_capacity_score", "mean"),
            mean_resilience_gap=("resilience_gap", "mean"),
            mean_justice_adjusted_vulnerability=("justice_adjusted_vulnerability", "mean"),
            mean_transformation_readiness=("transformation_readiness", "mean"),
        )
        .reset_index()
        .sort_values("mean_systemic_risk", ascending=False)
    )


def main() -> None:
    """Run the full advanced diagnostics workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "advanced_risk_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "advanced_risk_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "advanced_risk_resilience_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "advanced_risk_resilience_domain_summary.csv", index=False)

    print("\nAdvanced risk-resilience scores:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "hazard_type",
                "systemic_risk_score",
                "resilience_capacity_score",
                "resilience_gap",
                "justice_adjusted_vulnerability",
                "priority_class",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
