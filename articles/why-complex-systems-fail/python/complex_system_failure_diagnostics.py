"""
Advanced complex system failure diagnostics.

This workflow models complex system failure as an emergent result of:
- interdependence
- hidden coupling
- delayed feedback
- invisible deterioration
- buffer erosion
- loss of slack
- adaptation debt
- optimization pressure
- maintenance deficits
- monitoring gaps
- governance coordination limits
- social vulnerability
- critical-service dependence
- external stress
- cascading failure potential
- scenario-based resilience improvement
- Monte Carlo uncertainty around failure classification

The sample data are illustrative. Replace them with documented infrastructure,
governance, ecological, operational, and social indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/why-complex-systems-fail")
DATA_FILE = BASE_DIR / "data" / "complex_system_failure_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for failure-risk reduction and resilience upgrading."""

    name: str
    dependency_reduction: float
    coupling_reduction: float
    delay_reduction: float
    signal_visibility_gain: float
    buffer_gain: float
    redundancy_gain: float
    modularity_gain: float
    adaptation_debt_reduction: float
    optimization_pressure_reduction: float
    maintenance_gain: float
    monitoring_gain: float
    governance_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "monitoring_and_signal_upgrade": Scenario("monitoring_and_signal_upgrade", 0.02, 0.02, 0.10, 0.24, 0.06, 0.04, 0.04, 0.08, 0.04, 0.08, 0.24, 0.10),
    "redundancy_and_modularity": Scenario("redundancy_and_modularity", 0.10, 0.12, 0.04, 0.08, 0.18, 0.24, 0.24, 0.06, 0.08, 0.10, 0.08, 0.12),
    "deoptimization_for_resilience": Scenario("deoptimization_for_resilience", 0.08, 0.08, 0.04, 0.08, 0.20, 0.18, 0.16, 0.12, 0.24, 0.16, 0.10, 0.10),
    "adaptive_governance": Scenario("adaptive_governance", 0.06, 0.08, 0.12, 0.16, 0.12, 0.12, 0.14, 0.18, 0.12, 0.16, 0.18, 0.24),
    "system_resilience_portfolio": Scenario("system_resilience_portfolio", 0.14, 0.16, 0.16, 0.22, 0.24, 0.24, 0.24, 0.20, 0.22, 0.22, 0.24, 0.24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the complex-system-failure panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "dependency_density",
        "hidden_coupling",
        "feedback_delay",
        "signal_visibility",
        "buffer_capacity",
        "redundancy_capacity",
        "modularity_capacity",
        "adaptation_debt",
        "optimization_pressure",
        "maintenance_deficit",
        "monitoring_capacity",
        "governance_coordination",
        "social_vulnerability",
        "system_criticality",
        "external_stress",
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
    """Compute complex-system failure diagnostics."""
    scored = df.copy()

    scored["coupling_pressure"] = (
        0.48 * scored["dependency_density"]
        + 0.36 * scored["hidden_coupling"]
        + 0.16 * scored["system_criticality"]
    )

    scored["deterioration_pressure"] = (
        0.30 * scored["feedback_delay"]
        + 0.28 * (1 - scored["signal_visibility"])
        + 0.22 * scored["maintenance_deficit"]
        + 0.20 * scored["adaptation_debt"]
    )

    scored["slack_deficit"] = (
        0.34 * (1 - scored["buffer_capacity"])
        + 0.30 * (1 - scored["redundancy_capacity"])
        + 0.20 * (1 - scored["modularity_capacity"])
        + 0.16 * scored["optimization_pressure"]
    )

    scored["resilience_capacity"] = (
        0.20 * scored["buffer_capacity"]
        + 0.20 * scored["redundancy_capacity"]
        + 0.18 * scored["modularity_capacity"]
        + 0.18 * scored["monitoring_capacity"]
        + 0.14 * scored["governance_coordination"]
        + 0.10 * scored["signal_visibility"]
    )

    scored["cascade_potential"] = (
        scored["coupling_pressure"]
        * (1 + scored["external_stress"])
        * (1 + 0.5 * scored["system_criticality"])
        * (1 - 0.35 * scored["modularity_capacity"])
    )

    scored["structural_fragility"] = (
        0.30 * scored["coupling_pressure"]
        + 0.28 * scored["deterioration_pressure"]
        + 0.24 * scored["slack_deficit"]
        + 0.18 * scored["social_vulnerability"]
    )

    scored["failure_risk"] = (
        scored["structural_fragility"]
        * (1 + scored["external_stress"])
        * (1 + 0.35 * scored["system_criticality"])
        * (1 - 0.45 * scored["resilience_capacity"])
    )

    scored["failure_gap"] = np.maximum(
        0,
        scored["failure_risk"] - scored["resilience_capacity"],
    )

    scored["signal_gap"] = np.maximum(
        0,
        scored["deterioration_pressure"] - scored["monitoring_capacity"],
    )

    scored["resilience_priority_score"] = (
        0.35 * scored["failure_gap"]
        + 0.25 * scored["cascade_potential"].clip(0, 1)
        + 0.20 * scored["signal_gap"]
        + 0.20 * scored["social_vulnerability"]
    ).clip(0, 1)

    scored["failure_risk_band"] = scored["failure_risk"].apply(
        lambda x: classify_band(x, low=0.35, high=0.70)
    )

    scored["cascade_band"] = scored["cascade_potential"].apply(
        lambda x: classify_band(x, low=0.65, high=1.20)
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["cascade_potential"] > 1.20,
            scored["signal_gap"] > 0.25,
            scored["slack_deficit"] > 0.60,
            scored["adaptation_debt"] > 0.65,
        ],
        [
            "cascade_containment_priority",
            "monitoring_and_feedback_priority",
            "restore_slack_and_redundancy",
            "adaptation_debt_reduction",
        ],
        default="monitor_and_strengthen_resilience",
    )

    return scored.sort_values(
        ["resilience_priority_score", "failure_gap", "cascade_potential"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply failure-risk reduction scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["dependency_density"] = (
        scenario_df["dependency_density"] * (1 - scenario.dependency_reduction)
    ).clip(0, 1)

    scenario_df["hidden_coupling"] = (
        scenario_df["hidden_coupling"] * (1 - scenario.coupling_reduction)
    ).clip(0, 1)

    scenario_df["feedback_delay"] = (
        scenario_df["feedback_delay"] * (1 - scenario.delay_reduction)
    ).clip(0, 1)

    scenario_df["signal_visibility"] = (
        scenario_df["signal_visibility"] + scenario.signal_visibility_gain
    ).clip(0, 1)

    scenario_df["buffer_capacity"] = (
        scenario_df["buffer_capacity"] + scenario.buffer_gain
    ).clip(0, 1)

    scenario_df["redundancy_capacity"] = (
        scenario_df["redundancy_capacity"] + scenario.redundancy_gain
    ).clip(0, 1)

    scenario_df["modularity_capacity"] = (
        scenario_df["modularity_capacity"] + scenario.modularity_gain
    ).clip(0, 1)

    scenario_df["adaptation_debt"] = (
        scenario_df["adaptation_debt"] * (1 - scenario.adaptation_debt_reduction)
    ).clip(0, 1)

    scenario_df["optimization_pressure"] = (
        scenario_df["optimization_pressure"] * (1 - scenario.optimization_pressure_reduction)
    ).clip(0, 1)

    scenario_df["maintenance_deficit"] = (
        scenario_df["maintenance_deficit"] * (1 - scenario.maintenance_gain)
    ).clip(0, 1)

    scenario_df["monitoring_capacity"] = (
        scenario_df["monitoring_capacity"] + scenario.monitoring_gain
    ).clip(0, 1)

    scenario_df["governance_coordination"] = (
        scenario_df["governance_coordination"] + scenario.governance_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all failure-risk reduction scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around failure diagnostics."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "dependency_density",
        "hidden_coupling",
        "feedback_delay",
        "signal_visibility",
        "buffer_capacity",
        "redundancy_capacity",
        "modularity_capacity",
        "adaptation_debt",
        "optimization_pressure",
        "maintenance_deficit",
        "monitoring_capacity",
        "governance_coordination",
        "social_vulnerability",
        "system_criticality",
        "external_stress",
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
                    "coupling_pressure",
                    "deterioration_pressure",
                    "slack_deficit",
                    "resilience_capacity",
                    "cascade_potential",
                    "failure_risk",
                    "failure_gap",
                    "resilience_priority_score",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            coupling_p50=("coupling_pressure", "median"),
            deterioration_p50=("deterioration_pressure", "median"),
            slack_deficit_p50=("slack_deficit", "median"),
            resilience_capacity_p50=("resilience_capacity", "median"),
            cascade_p50=("cascade_potential", "median"),
            cascade_p95=("cascade_potential", lambda x: np.quantile(x, 0.95)),
            failure_risk_p50=("failure_risk", "median"),
            failure_gap_p50=("failure_gap", "median"),
            priority_p50=("resilience_priority_score", "median"),
        )
        .reset_index()
        .sort_values("priority_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize complex-system failure diagnostics by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_coupling_pressure=("coupling_pressure", "mean"),
            mean_deterioration_pressure=("deterioration_pressure", "mean"),
            mean_slack_deficit=("slack_deficit", "mean"),
            mean_resilience_capacity=("resilience_capacity", "mean"),
            mean_cascade_potential=("cascade_potential", "mean"),
            mean_failure_risk=("failure_risk", "mean"),
            mean_failure_gap=("failure_gap", "mean"),
            mean_priority_score=("resilience_priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_priority_score", ascending=False)
    )


def main() -> None:
    """Run the full complex-system failure diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "complex_system_failure_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "complex_system_failure_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "complex_system_failure_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "complex_system_failure_domain_summary.csv", index=False)

    print("\nComplex system failure diagnostics:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "coupling_pressure",
                "deterioration_pressure",
                "slack_deficit",
                "cascade_potential",
                "failure_risk",
                "failure_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
