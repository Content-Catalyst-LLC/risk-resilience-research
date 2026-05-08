"""
Advanced adaptation, recovery, and transformation diagnostics.

This workflow models:
- recovery as restoration of essential function after disruption
- adaptation as adjustment capacity under changing conditions
- transformation as readiness for structural change when recovery/adaptation are insufficient
- residual risk and maladaptation risk
- justice pressure and legitimacy constraints
- climate-resilient development pathway classification
- scenario-based response-pathway design
- Monte Carlo uncertainty around pathway classifications

The sample data are illustrative. Replace them with documented disaster,
infrastructure, climate, governance, ecological, and social indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/adaptation-recovery-transformation")
DATA_FILE = BASE_DIR / "data" / "adaptation_recovery_transformation_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for recovery, adaptation, and transformation planning."""

    name: str
    disruption_reduction: float
    recovery_gain: float
    adaptation_gain: float
    governance_gain: float
    learning_gain: float
    ecological_buffer_gain: float
    social_protection_gain: float
    transformation_gain: float
    maladaptation_reduction: float
    legitimacy_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "recovery_upgrade": Scenario("recovery_upgrade", 0.02, 0.22, 0.06, 0.08, 0.06, 0.04, 0.10, 0.04, 0.04, 0.08),
    "adaptive_pathways": Scenario("adaptive_pathways", 0.04, 0.08, 0.22, 0.16, 0.18, 0.14, 0.12, 0.10, 0.12, 0.12),
    "justice_centered_transformation": Scenario("justice_centered_transformation", 0.06, 0.10, 0.16, 0.20, 0.20, 0.18, 0.22, 0.28, 0.20, 0.22),
    "climate_resilient_development": Scenario("climate_resilient_development", 0.10, 0.18, 0.24, 0.24, 0.24, 0.24, 0.24, 0.26, 0.24, 0.24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the adaptation-recovery-transformation panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "disruption_severity",
        "recovery_capacity",
        "recovery_speed",
        "essential_function_restoration",
        "adaptive_capacity",
        "governance_capacity",
        "learning_capacity",
        "ecological_buffer_capacity",
        "social_protection_capacity",
        "transformation_readiness",
        "structural_unsustainability",
        "justice_pressure",
        "maladaptation_risk",
        "residual_risk",
        "public_legitimacy",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "domain", "region", "stress_type"}
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
    """Compute recovery, adaptation, transformation, and pathway diagnostics."""
    scored = df.copy()

    scored["recovery_score"] = (
        0.38 * scored["recovery_capacity"]
        + 0.28 * scored["recovery_speed"]
        + 0.34 * scored["essential_function_restoration"]
    )

    scored["adaptation_score"] = (
        0.26 * scored["adaptive_capacity"]
        + 0.22 * scored["governance_capacity"]
        + 0.18 * scored["learning_capacity"]
        + 0.18 * scored["ecological_buffer_capacity"]
        + 0.16 * scored["social_protection_capacity"]
    )

    scored["transformation_need"] = (
        0.36 * scored["structural_unsustainability"]
        + 0.26 * scored["justice_pressure"]
        + 0.22 * scored["residual_risk"]
        + 0.16 * scored["maladaptation_risk"]
    )

    scored["transformation_score"] = (
        0.34 * scored["transformation_readiness"]
        + 0.22 * scored["governance_capacity"]
        + 0.18 * scored["learning_capacity"]
        + 0.14 * scored["public_legitimacy"]
        + 0.12 * scored["social_protection_capacity"]
    )

    scored["response_capacity"] = (
        0.28 * scored["recovery_score"]
        + 0.36 * scored["adaptation_score"]
        + 0.24 * scored["transformation_score"]
        + 0.12 * scored["public_legitimacy"]
    )

    scored["pathway_gap"] = np.maximum(
        0,
        scored["disruption_severity"]
        + scored["residual_risk"]
        - scored["response_capacity"],
    )

    scored["maladaptation_adjusted_gap"] = (
        scored["pathway_gap"] * (1 + scored["maladaptation_risk"])
    )

    scored["transformational_threshold"] = np.maximum(
        0,
        scored["transformation_need"] - scored["transformation_score"],
    )

    scored["climate_resilient_development_score"] = (
        0.24 * scored["recovery_score"]
        + 0.30 * scored["adaptation_score"]
        + 0.26 * scored["transformation_score"]
        + 0.12 * scored["public_legitimacy"]
        + 0.08 * (1 - scored["maladaptation_risk"])
    ).clip(0, 1)

    scored["response_priority"] = np.select(
        [
            scored["disruption_severity"] > 0.78,
            scored["transformational_threshold"] > 0.22,
            scored["maladaptation_risk"] > 0.55,
            scored["adaptation_score"] < 0.48,
        ],
        [
            "urgent_recovery_with_risk_reduction",
            "transformation_planning_priority",
            "maladaptation_avoidance_priority",
            "adaptive_capacity_building",
        ],
        default="maintain_and_monitor_pathway",
    )

    scored["recovery_band"] = scored["recovery_score"].apply(
        lambda x: classify_band(x, low=0.40, high=0.65)
    )

    scored["adaptation_band"] = scored["adaptation_score"].apply(
        lambda x: classify_band(x, low=0.40, high=0.65)
    )

    scored["transformation_need_band"] = scored["transformation_need"].apply(
        lambda x: classify_band(x, low=0.35, high=0.60)
    )

    return scored.sort_values(
        ["maladaptation_adjusted_gap", "transformational_threshold", "disruption_severity"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply response-pathway scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["disruption_severity"] = (
        scenario_df["disruption_severity"] * (1 - scenario.disruption_reduction)
    ).clip(0, 1)

    for col in ["recovery_capacity", "recovery_speed", "essential_function_restoration"]:
        scenario_df[col] = (scenario_df[col] + scenario.recovery_gain).clip(0, 1)

    scenario_df["adaptive_capacity"] = (
        scenario_df["adaptive_capacity"] + scenario.adaptation_gain
    ).clip(0, 1)

    scenario_df["governance_capacity"] = (
        scenario_df["governance_capacity"] + scenario.governance_gain
    ).clip(0, 1)

    scenario_df["learning_capacity"] = (
        scenario_df["learning_capacity"] + scenario.learning_gain
    ).clip(0, 1)

    scenario_df["ecological_buffer_capacity"] = (
        scenario_df["ecological_buffer_capacity"] + scenario.ecological_buffer_gain
    ).clip(0, 1)

    scenario_df["social_protection_capacity"] = (
        scenario_df["social_protection_capacity"] + scenario.social_protection_gain
    ).clip(0, 1)

    scenario_df["transformation_readiness"] = (
        scenario_df["transformation_readiness"] + scenario.transformation_gain
    ).clip(0, 1)

    scenario_df["maladaptation_risk"] = (
        scenario_df["maladaptation_risk"] * (1 - scenario.maladaptation_reduction)
    ).clip(0, 1)

    scenario_df["public_legitimacy"] = (
        scenario_df["public_legitimacy"] + scenario.legitimacy_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all response-pathway scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around response pathway scores."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "disruption_severity",
        "recovery_capacity",
        "recovery_speed",
        "essential_function_restoration",
        "adaptive_capacity",
        "governance_capacity",
        "learning_capacity",
        "ecological_buffer_capacity",
        "social_protection_capacity",
        "transformation_readiness",
        "structural_unsustainability",
        "justice_pressure",
        "maladaptation_risk",
        "residual_risk",
        "public_legitimacy",
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
                    "recovery_score",
                    "adaptation_score",
                    "transformation_score",
                    "transformation_need",
                    "pathway_gap",
                    "maladaptation_adjusted_gap",
                    "climate_resilient_development_score",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            recovery_p50=("recovery_score", "median"),
            adaptation_p50=("adaptation_score", "median"),
            transformation_p50=("transformation_score", "median"),
            transformation_need_p50=("transformation_need", "median"),
            pathway_gap_p50=("pathway_gap", "median"),
            maladaptation_gap_p50=("maladaptation_adjusted_gap", "median"),
            climate_resilient_development_p50=("climate_resilient_development_score", "median"),
        )
        .reset_index()
        .sort_values("maladaptation_gap_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize recovery, adaptation, and transformation scores by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_recovery=("recovery_score", "mean"),
            mean_adaptation=("adaptation_score", "mean"),
            mean_transformation=("transformation_score", "mean"),
            mean_transformation_need=("transformation_need", "mean"),
            mean_pathway_gap=("pathway_gap", "mean"),
            mean_maladaptation_gap=("maladaptation_adjusted_gap", "mean"),
            mean_crd_score=("climate_resilient_development_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_maladaptation_gap", ascending=False)
    )


def main() -> None:
    """Run the full adaptation-recovery-transformation diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "adaptation_recovery_transformation_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "adaptation_recovery_transformation_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "adaptation_recovery_transformation_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "adaptation_recovery_transformation_domain_summary.csv", index=False)

    print("\nAdaptation, recovery, and transformation scores:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "recovery_score",
                "adaptation_score",
                "transformation_score",
                "transformation_need",
                "maladaptation_adjusted_gap",
                "response_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
