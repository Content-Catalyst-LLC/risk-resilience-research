"""
Advanced adaptive-cycle and panarchy diagnostics for social-ecological systems.

This workflow models:
- adaptive-cycle phase
- growth potential and connectedness
- rigidity and resilience capacity
- release pressure
- reorganization capacity
- novelty potential and memory capacity
- revolt and remember cross-scale dynamics
- inequality pressure
- institutional learning
- ecological buffer condition
- governance flexibility
- transformation readiness
- resilience traps
- justice-weighted reorganization gaps
- scenario-based reorganization strategies
- Monte Carlo uncertainty around adaptive-cycle classification

The sample data are illustrative. Replace them with documented social-ecological,
governance, infrastructure, climate, ecological, and community indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/adaptive-cycles-panarchy-social-ecological-systems")
DATA_FILE = BASE_DIR / "data" / "adaptive_cycles_panarchy_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for improving adaptive capacity and cross-scale reorganization."""

    name: str
    rigidity_reduction: float
    connectedness_rebalancing: float
    resilience_gain: float
    release_pressure_reduction: float
    reorganization_gain: float
    novelty_gain: float
    memory_gain: float
    revolt_reduction: float
    dependency_reduction: float
    inequality_reduction: float
    learning_gain: float
    ecological_buffer_gain: float
    governance_flexibility_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "memory_and_learning": Scenario("memory_and_learning", 0.08, 0.04, 0.12, 0.06, 0.14, 0.10, 0.24, 0.06, 0.06, 0.08, 0.28, 0.12, 0.14),
    "reorganization_capacity": Scenario("reorganization_capacity", 0.12, 0.08, 0.18, 0.10, 0.28, 0.24, 0.16, 0.08, 0.08, 0.10, 0.20, 0.18, 0.22),
    "anti_rigidity_transition": Scenario("anti_rigidity_transition", 0.24, 0.18, 0.20, 0.18, 0.22, 0.18, 0.16, 0.14, 0.14, 0.14, 0.22, 0.20, 0.26),
    "justice_centered_reorganization": Scenario("justice_centered_reorganization", 0.18, 0.12, 0.22, 0.14, 0.26, 0.24, 0.20, 0.18, 0.16, 0.28, 0.24, 0.22, 0.26),
    "panarchy_resilience_portfolio": Scenario("panarchy_resilience_portfolio", 0.28, 0.22, 0.30, 0.24, 0.30, 0.28, 0.28, 0.24, 0.24, 0.26, 0.30, 0.30, 0.30),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the adaptive-cycle and panarchy panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "scale_level",
        "domain",
        "region",
        "adaptive_phase",
        "growth_potential",
        "connectedness",
        "rigidity",
        "resilience_capacity",
        "release_pressure",
        "reorganization_capacity",
        "novelty_potential",
        "memory_capacity",
        "revolt_pressure",
        "cross_scale_dependency",
        "inequality_pressure",
        "institutional_learning",
        "ecological_buffer_condition",
        "governance_flexibility",
        "system_criticality",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "scale_level", "domain", "region", "adaptive_phase"}
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
    """Compute adaptive-cycle and panarchy diagnostics."""
    scored = df.copy()

    scored["conservation_rigidity_index"] = (
        0.34 * scored["connectedness"]
        + 0.34 * scored["rigidity"]
        + 0.18 * scored["cross_scale_dependency"]
        + 0.14 * (1 - scored["governance_flexibility"])
    )

    scored["release_risk_index"] = (
        0.34 * scored["release_pressure"]
        + 0.24 * scored["conservation_rigidity_index"]
        + 0.18 * scored["revolt_pressure"]
        + 0.14 * scored["system_criticality"]
        + 0.10 * scored["inequality_pressure"]
    )

    scored["reorganization_potential_index"] = (
        0.28 * scored["reorganization_capacity"]
        + 0.22 * scored["novelty_potential"]
        + 0.18 * scored["memory_capacity"]
        + 0.16 * scored["institutional_learning"]
        + 0.16 * scored["governance_flexibility"]
    )

    scored["remember_capacity"] = (
        0.34 * scored["memory_capacity"]
        + 0.24 * scored["institutional_learning"]
        + 0.22 * scored["ecological_buffer_condition"]
        + 0.20 * scored["governance_flexibility"]
    )

    scored["revolt_cascade_pressure"] = (
        scored["revolt_pressure"]
        * (1 + scored["cross_scale_dependency"])
        * (1 + 0.35 * scored["system_criticality"])
        * (1 - 0.35 * scored["remember_capacity"])
    )

    scored["resilience_trap_index"] = (
        0.32 * scored["conservation_rigidity_index"]
        + 0.24 * (1 - scored["reorganization_capacity"])
        + 0.18 * (1 - scored["novelty_potential"])
        + 0.16 * scored["inequality_pressure"]
        + 0.10 * scored["system_criticality"]
    )

    scored["transformation_readiness"] = (
        0.28 * scored["reorganization_potential_index"]
        + 0.24 * scored["resilience_capacity"]
        + 0.18 * scored["institutional_learning"]
        + 0.16 * scored["ecological_buffer_condition"]
        + 0.14 * scored["governance_flexibility"]
    )

    scored["justice_weighted_reorganization_gap"] = np.maximum(
        0,
        (
            0.32 * scored["release_risk_index"]
            + 0.26 * scored["revolt_cascade_pressure"]
            + 0.22 * scored["resilience_trap_index"]
            + 0.20 * scored["inequality_pressure"]
        )
        * (1 + 0.30 * scored["inequality_pressure"])
        - scored["transformation_readiness"],
    )

    scored["phase_stress_band"] = scored["release_risk_index"].apply(
        lambda x: classify_band(x, low=0.45, high=0.72)
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["conservation_rigidity_index"] > 0.72,
            scored["release_risk_index"] > 0.75,
            scored["reorganization_potential_index"] < 0.45,
            scored["revolt_cascade_pressure"] > 0.80,
            scored["resilience_trap_index"] > 0.70,
            scored["inequality_pressure"] > 0.70,
        ],
        [
            "anti_rigidity_transition",
            "release_pressure_management",
            "reorganization_capacity_building",
            "cross_scale_revolt_containment",
            "resilience_trap_escape",
            "justice_centered_reorganization",
        ],
        default="monitor_and_preserve_adaptive_capacity",
    )

    return scored.sort_values(
        ["justice_weighted_reorganization_gap", "release_risk_index", "resilience_trap_index"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply adaptive-cycle and panarchy scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["rigidity"] = (
        scenario_df["rigidity"] * (1 - scenario.rigidity_reduction)
    ).clip(0, 1)

    scenario_df["connectedness"] = (
        scenario_df["connectedness"] * (1 - scenario.connectedness_rebalancing)
    ).clip(0, 1)

    scenario_df["resilience_capacity"] = (
        scenario_df["resilience_capacity"] + scenario.resilience_gain
    ).clip(0, 1)

    scenario_df["release_pressure"] = (
        scenario_df["release_pressure"] * (1 - scenario.release_pressure_reduction)
    ).clip(0, 1)

    scenario_df["reorganization_capacity"] = (
        scenario_df["reorganization_capacity"] + scenario.reorganization_gain
    ).clip(0, 1)

    scenario_df["novelty_potential"] = (
        scenario_df["novelty_potential"] + scenario.novelty_gain
    ).clip(0, 1)

    scenario_df["memory_capacity"] = (
        scenario_df["memory_capacity"] + scenario.memory_gain
    ).clip(0, 1)

    scenario_df["revolt_pressure"] = (
        scenario_df["revolt_pressure"] * (1 - scenario.revolt_reduction)
    ).clip(0, 1)

    scenario_df["cross_scale_dependency"] = (
        scenario_df["cross_scale_dependency"] * (1 - scenario.dependency_reduction)
    ).clip(0, 1)

    scenario_df["inequality_pressure"] = (
        scenario_df["inequality_pressure"] * (1 - scenario.inequality_reduction)
    ).clip(0, 1)

    scenario_df["institutional_learning"] = (
        scenario_df["institutional_learning"] + scenario.learning_gain
    ).clip(0, 1)

    scenario_df["ecological_buffer_condition"] = (
        scenario_df["ecological_buffer_condition"] + scenario.ecological_buffer_gain
    ).clip(0, 1)

    scenario_df["governance_flexibility"] = (
        scenario_df["governance_flexibility"] + scenario.governance_flexibility_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all adaptive-cycle and panarchy scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around adaptive-cycle and panarchy scores."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "growth_potential",
        "connectedness",
        "rigidity",
        "resilience_capacity",
        "release_pressure",
        "reorganization_capacity",
        "novelty_potential",
        "memory_capacity",
        "revolt_pressure",
        "cross_scale_dependency",
        "inequality_pressure",
        "institutional_learning",
        "ecological_buffer_condition",
        "governance_flexibility",
        "system_criticality",
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
                    "conservation_rigidity_index",
                    "release_risk_index",
                    "reorganization_potential_index",
                    "remember_capacity",
                    "revolt_cascade_pressure",
                    "resilience_trap_index",
                    "transformation_readiness",
                    "justice_weighted_reorganization_gap",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            rigidity_p50=("conservation_rigidity_index", "median"),
            release_risk_p50=("release_risk_index", "median"),
            release_risk_p95=("release_risk_index", lambda x: np.quantile(x, 0.95)),
            reorganization_p50=("reorganization_potential_index", "median"),
            revolt_p50=("revolt_cascade_pressure", "median"),
            trap_p50=("resilience_trap_index", "median"),
            transformation_p50=("transformation_readiness", "median"),
            reorganization_gap_p50=("justice_weighted_reorganization_gap", "median"),
        )
        .reset_index()
        .sort_values("reorganization_gap_p50", ascending=False)
    )


def build_scale_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize adaptive-cycle and panarchy diagnostics by scale."""
    return (
        scored.groupby("scale_level")
        .agg(
            systems=("system_id", "count"),
            mean_rigidity=("conservation_rigidity_index", "mean"),
            mean_release_risk=("release_risk_index", "mean"),
            mean_reorganization=("reorganization_potential_index", "mean"),
            mean_remember_capacity=("remember_capacity", "mean"),
            mean_revolt_pressure=("revolt_cascade_pressure", "mean"),
            mean_trap=("resilience_trap_index", "mean"),
            mean_transformation=("transformation_readiness", "mean"),
            mean_reorganization_gap=("justice_weighted_reorganization_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_reorganization_gap", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize adaptive-cycle and panarchy diagnostics by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_rigidity=("conservation_rigidity_index", "mean"),
            mean_release_risk=("release_risk_index", "mean"),
            mean_reorganization=("reorganization_potential_index", "mean"),
            mean_transformation=("transformation_readiness", "mean"),
            mean_reorganization_gap=("justice_weighted_reorganization_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_reorganization_gap", ascending=False)
    )


def main() -> None:
    """Run the full adaptive-cycle and panarchy diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    scale_summary = build_scale_summary(scored)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "adaptive_cycles_panarchy_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "adaptive_cycles_panarchy_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "adaptive_cycles_panarchy_uncertainty.csv", index=False)
    scale_summary.to_csv(OUTPUT_DIR / "adaptive_cycles_panarchy_scale_summary.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "adaptive_cycles_panarchy_domain_summary.csv", index=False)

    print("\nAdaptive-cycle and panarchy diagnostics:")
    print(
        scored[
            [
                "system_name",
                "scale_level",
                "domain",
                "adaptive_phase",
                "conservation_rigidity_index",
                "release_risk_index",
                "reorganization_potential_index",
                "revolt_cascade_pressure",
                "transformation_readiness",
                "justice_weighted_reorganization_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nScale summary:")
    print(scale_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
