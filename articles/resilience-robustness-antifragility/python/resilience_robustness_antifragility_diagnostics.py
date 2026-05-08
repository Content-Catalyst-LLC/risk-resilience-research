"""
Advanced resilience, robustness, and antifragility diagnostics.

This workflow models:
- robustness as resistance to degradation
- resilience as recovery, adaptation, redundancy, modularity, and monitoring
- antifragility as bounded improvement through stress, learning, experimentation, optionality, and failure containment
- brittleness risk when stress exceeds resistance and response capacity
- justice constraints that prevent "learning from failure" from externalizing harm
- scenario-based system response design
- Monte Carlo uncertainty around system-response classifications

The sample data are illustrative. Replace them with documented infrastructure,
governance, social, ecological, and operational indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/resilience-robustness-antifragility")
DATA_FILE = BASE_DIR / "data" / "resilience_robustness_antifragility_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for system-response design."""

    name: str
    stress_reduction: float
    robustness_gain: float
    recovery_gain: float
    adaptive_gain: float
    redundancy_gain: float
    modularity_gain: float
    learning_gain: float
    experimentation_gain: float
    optionality_gain: float
    containment_gain: float
    justice_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "robustness_upgrade": Scenario("robustness_upgrade", 0.04, 0.24, 0.06, 0.04, 0.06, 0.04, 0.04, 0.02, 0.02, 0.08, 0.06),
    "resilience_upgrade": Scenario("resilience_upgrade", 0.04, 0.08, 0.20, 0.18, 0.18, 0.16, 0.12, 0.08, 0.08, 0.14, 0.12),
    "bounded_antifragility": Scenario("bounded_antifragility", 0.02, 0.04, 0.08, 0.16, 0.10, 0.18, 0.24, 0.26, 0.24, 0.22, 0.18),
    "sustainable_resilience_portfolio": Scenario("sustainable_resilience_portfolio", 0.08, 0.16, 0.20, 0.20, 0.20, 0.22, 0.22, 0.18, 0.20, 0.24, 0.24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the robustness-resilience-antifragility panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "stress_intensity",
        "stress_variability",
        "system_criticality",
        "robustness_capacity",
        "recovery_capacity",
        "adaptive_capacity",
        "redundancy_capacity",
        "modularity_capacity",
        "monitoring_capacity",
        "learning_capacity",
        "experimentation_capacity",
        "optionality_capacity",
        "failure_containment",
        "harm_bounding_capacity",
        "justice_safeguard_capacity",
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
    """Compute robustness, resilience, antifragility, brittleness, and suitability diagnostics."""
    scored = df.copy()

    scored["stress_load"] = (
        scored["stress_intensity"]
        * (1 + 0.5 * scored["stress_variability"])
        * (1 + 0.4 * scored["system_criticality"])
    )

    scored["robustness_score"] = scored["robustness_capacity"]

    scored["resilience_score"] = (
        0.23 * scored["recovery_capacity"]
        + 0.22 * scored["adaptive_capacity"]
        + 0.18 * scored["redundancy_capacity"]
        + 0.16 * scored["modularity_capacity"]
        + 0.11 * scored["monitoring_capacity"]
        + 0.10 * scored["failure_containment"]
    )

    scored["antifragility_potential"] = (
        0.24 * scored["learning_capacity"]
        + 0.22 * scored["experimentation_capacity"]
        + 0.20 * scored["optionality_capacity"]
        + 0.16 * scored["modularity_capacity"]
        + 0.10 * scored["failure_containment"]
        + 0.08 * scored["monitoring_capacity"]
    )

    scored["ethical_antifragility_limit"] = (
        0.42 * scored["harm_bounding_capacity"]
        + 0.36 * scored["justice_safeguard_capacity"]
        + 0.22 * scored["failure_containment"]
    )

    scored["bounded_antifragility_score"] = (
        scored["antifragility_potential"] * scored["ethical_antifragility_limit"]
    )

    scored["brittleness_risk"] = np.maximum(
        0,
        scored["stress_load"]
        - (
            0.42 * scored["robustness_score"]
            + 0.38 * scored["resilience_score"]
            + 0.20 * scored["ethical_antifragility_limit"]
        ),
    )

    scored["sustainable_resilience_score"] = (
        0.30 * scored["robustness_score"]
        + 0.42 * scored["resilience_score"]
        + 0.18 * scored["bounded_antifragility_score"]
        + 0.10 * scored["justice_safeguard_capacity"]
    )

    scored["system_response_gap"] = np.maximum(
        0,
        scored["stress_load"] - scored["sustainable_resilience_score"],
    )

    scored["robustness_need"] = np.maximum(
        0,
        scored["system_criticality"] - scored["robustness_score"],
    )

    scored["resilience_need"] = np.maximum(
        0,
        scored["stress_load"] - scored["resilience_score"],
    )

    scored["antifragility_suitability"] = (
        scored["bounded_antifragility_score"]
        * (1 - 0.55 * scored["system_criticality"])
        * scored["failure_containment"]
    ).clip(0, 1)

    scored["design_priority"] = np.select(
        [
            scored["system_criticality"] > 0.80,
            scored["brittleness_risk"] > 0.35,
            scored["antifragility_suitability"] > 0.20,
            scored["resilience_need"] > 0.30,
        ],
        [
            "robustness_for_critical_lifeline",
            "resilience_and_brittleness_reduction",
            "bounded_antifragile_learning",
            "adaptive_resilience_upgrade",
        ],
        default="balanced_monitoring_and_maintenance",
    )

    scored["stress_band"] = scored["stress_load"].apply(
        lambda x: classify_band(x, low=0.80, high=1.25)
    )

    scored["response_band"] = scored["sustainable_resilience_score"].apply(
        lambda x: classify_band(x, low=0.40, high=0.65)
    )

    return scored.sort_values(
        ["system_response_gap", "brittleness_risk", "stress_load"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply system-response design scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["stress_intensity"] = (
        scenario_df["stress_intensity"] * (1 - scenario.stress_reduction)
    ).clip(0, 1)

    scenario_df["robustness_capacity"] = (
        scenario_df["robustness_capacity"] + scenario.robustness_gain
    ).clip(0, 1)

    scenario_df["recovery_capacity"] = (
        scenario_df["recovery_capacity"] + scenario.recovery_gain
    ).clip(0, 1)

    scenario_df["adaptive_capacity"] = (
        scenario_df["adaptive_capacity"] + scenario.adaptive_gain
    ).clip(0, 1)

    scenario_df["redundancy_capacity"] = (
        scenario_df["redundancy_capacity"] + scenario.redundancy_gain
    ).clip(0, 1)

    scenario_df["modularity_capacity"] = (
        scenario_df["modularity_capacity"] + scenario.modularity_gain
    ).clip(0, 1)

    scenario_df["learning_capacity"] = (
        scenario_df["learning_capacity"] + scenario.learning_gain
    ).clip(0, 1)

    scenario_df["experimentation_capacity"] = (
        scenario_df["experimentation_capacity"] + scenario.experimentation_gain
    ).clip(0, 1)

    scenario_df["optionality_capacity"] = (
        scenario_df["optionality_capacity"] + scenario.optionality_gain
    ).clip(0, 1)

    scenario_df["failure_containment"] = (
        scenario_df["failure_containment"] + scenario.containment_gain
    ).clip(0, 1)

    scenario_df["harm_bounding_capacity"] = (
        scenario_df["harm_bounding_capacity"] + scenario.containment_gain
    ).clip(0, 1)

    scenario_df["justice_safeguard_capacity"] = (
        scenario_df["justice_safeguard_capacity"] + scenario.justice_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all system-response design scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around system-response scores."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "stress_intensity",
        "stress_variability",
        "system_criticality",
        "robustness_capacity",
        "recovery_capacity",
        "adaptive_capacity",
        "redundancy_capacity",
        "modularity_capacity",
        "monitoring_capacity",
        "learning_capacity",
        "experimentation_capacity",
        "optionality_capacity",
        "failure_containment",
        "harm_bounding_capacity",
        "justice_safeguard_capacity",
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
                    "robustness_score",
                    "resilience_score",
                    "bounded_antifragility_score",
                    "brittleness_risk",
                    "sustainable_resilience_score",
                    "system_response_gap",
                    "antifragility_suitability",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            robustness_p50=("robustness_score", "median"),
            resilience_p50=("resilience_score", "median"),
            antifragility_p50=("bounded_antifragility_score", "median"),
            brittleness_p50=("brittleness_risk", "median"),
            brittleness_p95=("brittleness_risk", lambda x: np.quantile(x, 0.95)),
            sustainable_resilience_p50=("sustainable_resilience_score", "median"),
            response_gap_p50=("system_response_gap", "median"),
            antifragility_suitability_p50=("antifragility_suitability", "median"),
        )
        .reset_index()
        .sort_values("response_gap_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize system-response scores by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_stress_load=("stress_load", "mean"),
            mean_robustness=("robustness_score", "mean"),
            mean_resilience=("resilience_score", "mean"),
            mean_bounded_antifragility=("bounded_antifragility_score", "mean"),
            mean_brittleness_risk=("brittleness_risk", "mean"),
            mean_sustainable_resilience=("sustainable_resilience_score", "mean"),
            mean_response_gap=("system_response_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_response_gap", ascending=False)
    )


def main() -> None:
    """Run the full robustness-resilience-antifragility diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "resilience_robustness_antifragility_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "resilience_robustness_antifragility_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "resilience_robustness_antifragility_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "resilience_robustness_antifragility_domain_summary.csv", index=False)

    print("\nResilience, robustness, and antifragility scores:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "stress_load",
                "robustness_score",
                "resilience_score",
                "bounded_antifragility_score",
                "brittleness_risk",
                "system_response_gap",
                "design_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
