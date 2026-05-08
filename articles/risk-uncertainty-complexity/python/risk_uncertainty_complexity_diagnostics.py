"""
Advanced risk, uncertainty, and complexity diagnostics.

This workflow models:
- expected risk
- uncertainty-adjusted risk
- complexity amplification
- systemic risk
- robust response capacity
- resilience gaps
- scenario-based governance improvement
- Monte Carlo uncertainty around system risk
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/risk-uncertainty-complexity")
DATA_FILE = BASE_DIR / "data" / "risk_uncertainty_complexity_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    name: str
    probability_reduction: float
    loss_reduction: float
    uncertainty_reduction: float
    dependency_reduction: float
    monitoring_gain: float
    redundancy_gain: float
    flexibility_gain: float
    learning_gain: float
    adaptive_governance_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "monitoring_upgrade": Scenario("monitoring_upgrade", 0.02, 0.02, 0.18, 0.02, 0.20, 0.04, 0.06, 0.08, 0.08),
    "redundancy_and_modularity": Scenario("redundancy_and_modularity", 0.03, 0.06, 0.06, 0.16, 0.06, 0.22, 0.18, 0.08, 0.08),
    "adaptive_governance": Scenario("adaptive_governance", 0.04, 0.08, 0.10, 0.08, 0.12, 0.10, 0.16, 0.20, 0.22),
    "deep_robustness_transition": Scenario("deep_robustness_transition", 0.08, 0.14, 0.18, 0.20, 0.20, 0.24, 0.24, 0.24, 0.26),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the risk-uncertainty-complexity panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "primary_hazard",
        "hazard_probability",
        "expected_loss_index",
        "probability_uncertainty",
        "loss_uncertainty",
        "dependency_density",
        "feedback_strength",
        "threshold_sensitivity",
        "adaptive_behavior",
        "monitoring_capacity",
        "redundancy_capacity",
        "flexibility_capacity",
        "institutional_learning",
        "adaptive_governance_capacity",
        "social_vulnerability",
        "criticality_index",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "domain", "region", "primary_hazard"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def classify_band(value: float, low: float, high: float) -> str:
    """Classify normalized values."""
    if value < low:
        return "lower"
    if value < high:
        return "moderate"
    return "elevated"


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute risk, uncertainty, complexity, systemic risk, and resilience gaps."""
    scored = df.copy()

    scored["expected_risk"] = (
        scored["hazard_probability"] * scored["expected_loss_index"]
    )

    scored["combined_uncertainty"] = (
        scored["probability_uncertainty"] + scored["loss_uncertainty"]
    ) / 2

    scored["uncertainty_adjusted_risk"] = (
        scored["expected_risk"] * (1 + scored["combined_uncertainty"])
    )

    scored["complexity_multiplier"] = (
        1
        + 0.28 * scored["dependency_density"]
        + 0.24 * scored["feedback_strength"]
        + 0.24 * scored["threshold_sensitivity"]
        + 0.24 * scored["adaptive_behavior"]
    )

    scored["systemic_risk"] = (
        scored["uncertainty_adjusted_risk"] * scored["complexity_multiplier"]
    )

    scored["robust_response_capacity"] = (
        0.22 * scored["monitoring_capacity"]
        + 0.20 * scored["redundancy_capacity"]
        + 0.18 * scored["flexibility_capacity"]
        + 0.20 * scored["institutional_learning"]
        + 0.20 * scored["adaptive_governance_capacity"]
    )

    scored["vulnerability_weighted_systemic_risk"] = (
        scored["systemic_risk"]
        * (1 + 0.30 * scored["social_vulnerability"])
        * (1 + 0.20 * scored["criticality_index"])
    )

    scored["resilience_gap"] = np.maximum(
        0,
        scored["vulnerability_weighted_systemic_risk"]
        - scored["robust_response_capacity"],
    )

    scored["risk_band"] = scored["vulnerability_weighted_systemic_risk"].apply(
        lambda x: classify_band(x, low=0.25, high=0.55)
    )

    scored["capacity_band"] = scored["robust_response_capacity"].apply(
        lambda x: classify_band(x, low=0.40, high=0.65)
    )

    scored["priority_class"] = np.select(
        [
            (scored["risk_band"] == "elevated") & (scored["capacity_band"] != "elevated"),
            scored["combined_uncertainty"] > 0.45,
            scored["complexity_multiplier"] > 1.65,
            scored["resilience_gap"] > 0.20,
        ],
        [
            "urgent_systemic_risk_reduction",
            "uncertainty_management_priority",
            "complexity_governance_priority",
            "capacity_building_priority",
        ],
        default="monitor_and_learn",
    )

    return scored.sort_values(
        ["vulnerability_weighted_systemic_risk", "resilience_gap"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["hazard_probability"] = (
        scenario_df["hazard_probability"] * (1 - scenario.probability_reduction)
    ).clip(0, 1)

    scenario_df["expected_loss_index"] = (
        scenario_df["expected_loss_index"] * (1 - scenario.loss_reduction)
    ).clip(0, 1)

    for col in ["probability_uncertainty", "loss_uncertainty"]:
        scenario_df[col] = (
            scenario_df[col] * (1 - scenario.uncertainty_reduction)
        ).clip(0, 1)

    scenario_df["dependency_density"] = (
        scenario_df["dependency_density"] * (1 - scenario.dependency_reduction)
    ).clip(0, 1)

    scenario_df["monitoring_capacity"] = (
        scenario_df["monitoring_capacity"] + scenario.monitoring_gain
    ).clip(0, 1)

    scenario_df["redundancy_capacity"] = (
        scenario_df["redundancy_capacity"] + scenario.redundancy_gain
    ).clip(0, 1)

    scenario_df["flexibility_capacity"] = (
        scenario_df["flexibility_capacity"] + scenario.flexibility_gain
    ).clip(0, 1)

    scenario_df["institutional_learning"] = (
        scenario_df["institutional_learning"] + scenario.learning_gain
    ).clip(0, 1)

    scenario_df["adaptive_governance_capacity"] = (
        scenario_df["adaptive_governance_capacity"] + scenario.adaptive_governance_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all governance scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around system indicators."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "hazard_probability",
        "expected_loss_index",
        "probability_uncertainty",
        "loss_uncertainty",
        "dependency_density",
        "feedback_strength",
        "threshold_sensitivity",
        "adaptive_behavior",
        "monitoring_capacity",
        "redundancy_capacity",
        "flexibility_capacity",
        "institutional_learning",
        "adaptive_governance_capacity",
        "social_vulnerability",
        "criticality_index",
    ]

    for draw in range(draws):
        sampled = df.copy()
        noise = rng.normal(loc=0.0, scale=0.04, size=(len(df), len(numeric_cols)))
        sampled[numeric_cols] = np.clip(sampled[numeric_cols].to_numpy() + noise, 0, 1)

        scored = score_systems(sampled)
        scored["draw"] = draw

        records.append(
            scored[
                [
                    "system_id",
                    "system_name",
                    "draw",
                    "vulnerability_weighted_systemic_risk",
                    "robust_response_capacity",
                    "resilience_gap",
                    "combined_uncertainty",
                    "complexity_multiplier",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            risk_p05=("vulnerability_weighted_systemic_risk", lambda x: np.quantile(x, 0.05)),
            risk_p50=("vulnerability_weighted_systemic_risk", "median"),
            risk_p95=("vulnerability_weighted_systemic_risk", lambda x: np.quantile(x, 0.95)),
            capacity_p50=("robust_response_capacity", "median"),
            gap_p50=("resilience_gap", "median"),
            uncertainty_p50=("combined_uncertainty", "median"),
            complexity_p50=("complexity_multiplier", "median"),
        )
        .reset_index()
        .sort_values("risk_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize risk, uncertainty, and complexity by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_expected_risk=("expected_risk", "mean"),
            mean_uncertainty_adjusted_risk=("uncertainty_adjusted_risk", "mean"),
            mean_complexity_multiplier=("complexity_multiplier", "mean"),
            mean_systemic_risk=("vulnerability_weighted_systemic_risk", "mean"),
            mean_response_capacity=("robust_response_capacity", "mean"),
            mean_resilience_gap=("resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_systemic_risk", ascending=False)
    )


def main() -> None:
    """Run the full diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "risk_uncertainty_complexity_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "risk_uncertainty_complexity_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "risk_uncertainty_complexity_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "risk_uncertainty_complexity_domain_summary.csv", index=False)

    print("\nRisk, uncertainty, and complexity scores:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "primary_hazard",
                "uncertainty_adjusted_risk",
                "complexity_multiplier",
                "vulnerability_weighted_systemic_risk",
                "robust_response_capacity",
                "resilience_gap",
                "priority_class",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
