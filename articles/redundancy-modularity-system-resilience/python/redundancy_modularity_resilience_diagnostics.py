"""
Advanced redundancy, modularity, and system-resilience diagnostics.

This workflow models:
- primary failure pressure
- redundancy capacity
- modularity capacity
- backup diversity
- pathway diversity
- spare capacity
- coupling intensity
- dependency concentration
- containment strength
- restoration capacity
- monitoring capacity
- governance coordination
- social vulnerability
- system criticality
- efficiency pressure
- continuity capacity
- propagation reduction
- justice-weighted resilience gaps
- scenario-based design improvements
- Monte Carlo uncertainty around resilience classification

The sample data are illustrative. Replace them with documented infrastructure,
network, governance, dependency, maintenance, social vulnerability, and continuity
data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/redundancy-modularity-system-resilience")
DATA_FILE = BASE_DIR / "data" / "redundancy_modularity_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for improving redundancy, modularity, and containment."""

    name: str
    failure_pressure_reduction: float
    redundancy_gain: float
    modularity_gain: float
    backup_diversity_gain: float
    pathway_diversity_gain: float
    spare_capacity_gain: float
    coupling_reduction: float
    dependency_reduction: float
    containment_gain: float
    restoration_gain: float
    monitoring_gain: float
    governance_gain: float
    vulnerability_reduction: float
    efficiency_pressure_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "redundancy_rebuild": Scenario("redundancy_rebuild", 0.06, 0.28, 0.10, 0.24, 0.22, 0.24, 0.08, 0.10, 0.10, 0.12, 0.10, 0.10, 0.08, 0.12),
    "modularity_and_containment": Scenario("modularity_and_containment", 0.06, 0.10, 0.30, 0.10, 0.16, 0.12, 0.22, 0.20, 0.30, 0.12, 0.12, 0.16, 0.08, 0.10),
    "continuity_and_restoration": Scenario("continuity_and_restoration", 0.08, 0.18, 0.18, 0.16, 0.18, 0.18, 0.12, 0.12, 0.18, 0.28, 0.18, 0.24, 0.12, 0.12),
    "justice_centered_resilience_design": Scenario("justice_centered_resilience_design", 0.10, 0.20, 0.20, 0.18, 0.20, 0.20, 0.14, 0.14, 0.20, 0.20, 0.20, 0.24, 0.26, 0.16),
    "resilience_design_portfolio": Scenario("resilience_design_portfolio", 0.18, 0.30, 0.30, 0.28, 0.28, 0.28, 0.26, 0.26, 0.30, 0.30, 0.28, 0.28, 0.24, 0.24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the redundancy-modularity panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "primary_failure_pressure",
        "redundancy_capacity",
        "modularity_capacity",
        "backup_diversity",
        "pathway_diversity",
        "spare_capacity",
        "coupling_intensity",
        "dependency_concentration",
        "containment_strength",
        "restoration_capacity",
        "monitoring_capacity",
        "governance_coordination",
        "social_vulnerability",
        "system_criticality",
        "efficiency_pressure",
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
    """Compute redundancy, modularity, containment, continuity, and resilience-gap scores."""
    scored = df.copy()

    scored["redundancy_index"] = (
        0.32 * scored["redundancy_capacity"]
        + 0.24 * scored["backup_diversity"]
        + 0.22 * scored["pathway_diversity"]
        + 0.22 * scored["spare_capacity"]
    )

    scored["modularity_index"] = (
        0.42 * scored["modularity_capacity"]
        + 0.28 * scored["containment_strength"]
        + 0.18 * (1 - scored["coupling_intensity"])
        + 0.12 * (1 - scored["dependency_concentration"])
    )

    scored["resilience_design_capacity"] = (
        0.30 * scored["redundancy_index"]
        + 0.30 * scored["modularity_index"]
        + 0.16 * scored["restoration_capacity"]
        + 0.14 * scored["monitoring_capacity"]
        + 0.10 * scored["governance_coordination"]
    )

    scored["propagation_pressure"] = (
        scored["primary_failure_pressure"]
        * (1 + scored["coupling_intensity"])
        * (1 + scored["dependency_concentration"])
        * (1 + 0.25 * scored["system_criticality"])
        * (1 - 0.45 * scored["modularity_index"])
    )

    scored["continuity_capacity"] = (
        0.28 * scored["redundancy_index"]
        + 0.22 * scored["restoration_capacity"]
        + 0.20 * scored["governance_coordination"]
        + 0.16 * scored["monitoring_capacity"]
        + 0.14 * scored["containment_strength"]
    )

    scored["efficiency_fragility_pressure"] = (
        0.34 * scored["efficiency_pressure"]
        + 0.22 * (1 - scored["redundancy_capacity"])
        + 0.22 * (1 - scored["modularity_capacity"])
        + 0.22 * scored["dependency_concentration"]
    )

    scored["justice_weighted_resilience_gap"] = np.maximum(
        0,
        (
            0.34 * scored["propagation_pressure"]
            + 0.28 * scored["efficiency_fragility_pressure"]
            + 0.22 * scored["social_vulnerability"]
            + 0.16 * scored["system_criticality"]
        )
        * (1 + 0.30 * scored["social_vulnerability"])
        - scored["continuity_capacity"],
    )

    scored["resilience_band"] = scored["resilience_design_capacity"].apply(
        lambda x: classify_band(x, low=0.42, high=0.68)
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["redundancy_index"] < 0.42,
            scored["modularity_index"] < 0.42,
            scored["propagation_pressure"] > 1.40,
            scored["continuity_capacity"] < 0.45,
            scored["efficiency_fragility_pressure"] > 0.72,
            scored["social_vulnerability"] > 0.72,
        ],
        [
            "redundancy_rebuild_priority",
            "modularity_and_containment_priority",
            "propagation_reduction_priority",
            "essential_function_continuity_gap",
            "deoptimization_for_resilience",
            "justice_centered_resilience_design",
        ],
        default="monitor_and_preserve_resilience_design",
    )

    return scored.sort_values(
        ["justice_weighted_resilience_gap", "propagation_pressure", "efficiency_fragility_pressure"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply redundancy-modularity scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["primary_failure_pressure"] = (
        scenario_df["primary_failure_pressure"] * (1 - scenario.failure_pressure_reduction)
    ).clip(0, 1)

    scenario_df["redundancy_capacity"] = (
        scenario_df["redundancy_capacity"] + scenario.redundancy_gain
    ).clip(0, 1)

    scenario_df["modularity_capacity"] = (
        scenario_df["modularity_capacity"] + scenario.modularity_gain
    ).clip(0, 1)

    scenario_df["backup_diversity"] = (
        scenario_df["backup_diversity"] + scenario.backup_diversity_gain
    ).clip(0, 1)

    scenario_df["pathway_diversity"] = (
        scenario_df["pathway_diversity"] + scenario.pathway_diversity_gain
    ).clip(0, 1)

    scenario_df["spare_capacity"] = (
        scenario_df["spare_capacity"] + scenario.spare_capacity_gain
    ).clip(0, 1)

    scenario_df["coupling_intensity"] = (
        scenario_df["coupling_intensity"] * (1 - scenario.coupling_reduction)
    ).clip(0, 1)

    scenario_df["dependency_concentration"] = (
        scenario_df["dependency_concentration"] * (1 - scenario.dependency_reduction)
    ).clip(0, 1)

    scenario_df["containment_strength"] = (
        scenario_df["containment_strength"] + scenario.containment_gain
    ).clip(0, 1)

    scenario_df["restoration_capacity"] = (
        scenario_df["restoration_capacity"] + scenario.restoration_gain
    ).clip(0, 1)

    scenario_df["monitoring_capacity"] = (
        scenario_df["monitoring_capacity"] + scenario.monitoring_gain
    ).clip(0, 1)

    scenario_df["governance_coordination"] = (
        scenario_df["governance_coordination"] + scenario.governance_gain
    ).clip(0, 1)

    scenario_df["social_vulnerability"] = (
        scenario_df["social_vulnerability"] * (1 - scenario.vulnerability_reduction)
    ).clip(0, 1)

    scenario_df["efficiency_pressure"] = (
        scenario_df["efficiency_pressure"] * (1 - scenario.efficiency_pressure_reduction)
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all redundancy-modularity scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around redundancy-modularity scores."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "primary_failure_pressure",
        "redundancy_capacity",
        "modularity_capacity",
        "backup_diversity",
        "pathway_diversity",
        "spare_capacity",
        "coupling_intensity",
        "dependency_concentration",
        "containment_strength",
        "restoration_capacity",
        "monitoring_capacity",
        "governance_coordination",
        "social_vulnerability",
        "system_criticality",
        "efficiency_pressure",
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
                    "redundancy_index",
                    "modularity_index",
                    "resilience_design_capacity",
                    "propagation_pressure",
                    "continuity_capacity",
                    "efficiency_fragility_pressure",
                    "justice_weighted_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            redundancy_p50=("redundancy_index", "median"),
            modularity_p50=("modularity_index", "median"),
            design_capacity_p50=("resilience_design_capacity", "median"),
            propagation_p50=("propagation_pressure", "median"),
            propagation_p95=("propagation_pressure", lambda x: np.quantile(x, 0.95)),
            continuity_p50=("continuity_capacity", "median"),
            resilience_gap_p50=("justice_weighted_resilience_gap", "median"),
            resilience_gap_p95=("justice_weighted_resilience_gap", lambda x: np.quantile(x, 0.95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize redundancy-modularity diagnostics by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_redundancy=("redundancy_index", "mean"),
            mean_modularity=("modularity_index", "mean"),
            mean_design_capacity=("resilience_design_capacity", "mean"),
            mean_propagation_pressure=("propagation_pressure", "mean"),
            mean_continuity_capacity=("continuity_capacity", "mean"),
            mean_efficiency_fragility=("efficiency_fragility_pressure", "mean"),
            mean_resilience_gap=("justice_weighted_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )


def main() -> None:
    """Run the full redundancy-modularity diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "redundancy_modularity_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "redundancy_modularity_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "redundancy_modularity_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "redundancy_modularity_domain_summary.csv", index=False)

    print("\nRedundancy, modularity, and system-resilience diagnostics:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "redundancy_index",
                "modularity_index",
                "resilience_design_capacity",
                "propagation_pressure",
                "continuity_capacity",
                "justice_weighted_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
