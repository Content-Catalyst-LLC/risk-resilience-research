"""
Advanced cascading-failure diagnostics for interdependent systems.

This workflow models:
- initiating shock severity
- dependency density and hidden coupling
- critical-node exposure
- backup, modularity, and redundancy capacity
- cross-sector coordination and restoration speed
- propagation likelihood
- cascade amplification
- essential-function continuity
- justice-weighted cascade risk
- scenario-based containment strategies
- Monte Carlo uncertainty around cascade classification

The sample data are illustrative. Replace them with documented infrastructure,
governance, dependency, service-continuity, and community vulnerability data before
applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/cascading-failures-interdependent-systems")
DATA_FILE = BASE_DIR / "data" / "cascading_failures_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for cascade containment and continuity protection."""

    name: str
    shock_reduction: float
    dependency_reduction: float
    coupling_reduction: float
    critical_node_reduction: float
    backup_gain: float
    modularity_gain: float
    coordination_gain: float
    restoration_gain: float
    redundancy_gain: float
    vulnerability_reduction: float
    governance_gain: float
    cascade_exposure_reduction: float
    monitoring_gain: float
    trust_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "dependency_mapping_and_monitoring": Scenario("dependency_mapping_and_monitoring", 0.04, 0.06, 0.10, 0.08, 0.06, 0.06, 0.14, 0.08, 0.06, 0.06, 0.12, 0.08, 0.26, 0.10),
    "modularity_and_redundancy": Scenario("modularity_and_redundancy", 0.06, 0.12, 0.12, 0.12, 0.22, 0.26, 0.12, 0.12, 0.26, 0.08, 0.12, 0.14, 0.10, 0.08),
    "critical_node_hardening": Scenario("critical_node_hardening", 0.10, 0.10, 0.12, 0.26, 0.20, 0.18, 0.14, 0.18, 0.18, 0.10, 0.16, 0.16, 0.14, 0.12),
    "cross_sector_continuity": Scenario("cross_sector_continuity", 0.08, 0.10, 0.10, 0.12, 0.18, 0.18, 0.28, 0.26, 0.18, 0.12, 0.24, 0.18, 0.20, 0.18),
    "justice_centered_containment": Scenario("justice_centered_containment", 0.10, 0.12, 0.12, 0.14, 0.20, 0.20, 0.24, 0.22, 0.20, 0.26, 0.24, 0.20, 0.20, 0.24),
    "systemic_resilience_portfolio": Scenario("systemic_resilience_portfolio", 0.18, 0.24, 0.24, 0.26, 0.30, 0.30, 0.30, 0.30, 0.30, 0.24, 0.30, 0.28, 0.28, 0.26),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the cascading-failure panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "initiating_shock_severity",
        "dependency_density",
        "hidden_coupling",
        "critical_node_exposure",
        "backup_capacity",
        "modularity_capacity",
        "cross_sector_coordination",
        "restoration_speed",
        "redundancy_capacity",
        "social_vulnerability",
        "governance_readiness",
        "system_criticality",
        "cascade_exposure",
        "monitoring_capacity",
        "public_trust",
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
    """Compute cascade propagation, continuity, and justice-weighted risk scores."""
    scored = df.copy()

    scored["dependency_pressure"] = (
        0.34 * scored["dependency_density"]
        + 0.30 * scored["hidden_coupling"]
        + 0.22 * scored["critical_node_exposure"]
        + 0.14 * scored["system_criticality"]
    )

    scored["containment_capacity"] = (
        0.22 * scored["backup_capacity"]
        + 0.24 * scored["modularity_capacity"]
        + 0.20 * scored["redundancy_capacity"]
        + 0.18 * scored["monitoring_capacity"]
        + 0.16 * scored["cross_sector_coordination"]
    )

    scored["governance_response_capacity"] = (
        0.30 * scored["cross_sector_coordination"]
        + 0.24 * scored["restoration_speed"]
        + 0.20 * scored["governance_readiness"]
        + 0.14 * scored["monitoring_capacity"]
        + 0.12 * scored["public_trust"]
    )

    scored["propagation_likelihood"] = (
        scored["initiating_shock_severity"]
        * (1 + scored["dependency_pressure"])
        * (1 + 0.35 * scored["cascade_exposure"])
        * (1 - 0.45 * scored["containment_capacity"])
    )

    scored["cascade_amplification"] = (
        scored["propagation_likelihood"]
        * (1 + scored["system_criticality"])
        * (1 + scored["social_vulnerability"])
        * (1 - 0.35 * scored["governance_response_capacity"])
    )

    scored["essential_function_continuity"] = (
        0.26 * scored["backup_capacity"]
        + 0.22 * scored["redundancy_capacity"]
        + 0.20 * scored["restoration_speed"]
        + 0.18 * scored["cross_sector_coordination"]
        + 0.14 * scored["public_trust"]
    )

    scored["continuity_gap"] = np.maximum(
        0,
        scored["cascade_amplification"] - scored["essential_function_continuity"],
    )

    scored["justice_weighted_cascade_risk"] = (
        0.34 * scored["propagation_likelihood"]
        + 0.30 * scored["cascade_amplification"]
        + 0.20 * scored["continuity_gap"]
        + 0.16 * scored["social_vulnerability"]
    ) * (1 + 0.30 * scored["social_vulnerability"])

    scored["cascade_band"] = scored["justice_weighted_cascade_risk"].apply(
        lambda x: classify_band(x, low=0.55, high=1.05)
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["dependency_pressure"] > 0.78,
            scored["critical_node_exposure"] > 0.78,
            scored["containment_capacity"] < 0.42,
            scored["governance_response_capacity"] < 0.45,
            scored["continuity_gap"] > 0.45,
            scored["social_vulnerability"] > 0.72,
        ],
        [
            "dependency_mapping_priority",
            "critical_node_hardening",
            "modularity_and_redundancy_rebuild",
            "cross_sector_governance_priority",
            "essential_function_continuity_gap",
            "justice_centered_containment",
        ],
        default="monitor_and_strengthen_containment",
    )

    return scored.sort_values(
        ["justice_weighted_cascade_risk", "continuity_gap", "cascade_amplification"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply cascade-containment scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["initiating_shock_severity"] = (
        scenario_df["initiating_shock_severity"] * (1 - scenario.shock_reduction)
    ).clip(0, 1)

    scenario_df["dependency_density"] = (
        scenario_df["dependency_density"] * (1 - scenario.dependency_reduction)
    ).clip(0, 1)

    scenario_df["hidden_coupling"] = (
        scenario_df["hidden_coupling"] * (1 - scenario.coupling_reduction)
    ).clip(0, 1)

    scenario_df["critical_node_exposure"] = (
        scenario_df["critical_node_exposure"] * (1 - scenario.critical_node_reduction)
    ).clip(0, 1)

    scenario_df["backup_capacity"] = (
        scenario_df["backup_capacity"] + scenario.backup_gain
    ).clip(0, 1)

    scenario_df["modularity_capacity"] = (
        scenario_df["modularity_capacity"] + scenario.modularity_gain
    ).clip(0, 1)

    scenario_df["cross_sector_coordination"] = (
        scenario_df["cross_sector_coordination"] + scenario.coordination_gain
    ).clip(0, 1)

    scenario_df["restoration_speed"] = (
        scenario_df["restoration_speed"] + scenario.restoration_gain
    ).clip(0, 1)

    scenario_df["redundancy_capacity"] = (
        scenario_df["redundancy_capacity"] + scenario.redundancy_gain
    ).clip(0, 1)

    scenario_df["social_vulnerability"] = (
        scenario_df["social_vulnerability"] * (1 - scenario.vulnerability_reduction)
    ).clip(0, 1)

    scenario_df["governance_readiness"] = (
        scenario_df["governance_readiness"] + scenario.governance_gain
    ).clip(0, 1)

    scenario_df["cascade_exposure"] = (
        scenario_df["cascade_exposure"] * (1 - scenario.cascade_exposure_reduction)
    ).clip(0, 1)

    scenario_df["monitoring_capacity"] = (
        scenario_df["monitoring_capacity"] + scenario.monitoring_gain
    ).clip(0, 1)

    scenario_df["public_trust"] = (
        scenario_df["public_trust"] + scenario.trust_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all cascade-containment scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around cascade-risk scores."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "initiating_shock_severity",
        "dependency_density",
        "hidden_coupling",
        "critical_node_exposure",
        "backup_capacity",
        "modularity_capacity",
        "cross_sector_coordination",
        "restoration_speed",
        "redundancy_capacity",
        "social_vulnerability",
        "governance_readiness",
        "system_criticality",
        "cascade_exposure",
        "monitoring_capacity",
        "public_trust",
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
                    "dependency_pressure",
                    "containment_capacity",
                    "governance_response_capacity",
                    "propagation_likelihood",
                    "cascade_amplification",
                    "essential_function_continuity",
                    "continuity_gap",
                    "justice_weighted_cascade_risk",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            dependency_pressure_p50=("dependency_pressure", "median"),
            containment_capacity_p50=("containment_capacity", "median"),
            propagation_p50=("propagation_likelihood", "median"),
            cascade_amplification_p50=("cascade_amplification", "median"),
            cascade_amplification_p95=("cascade_amplification", lambda x: np.quantile(x, 0.95)),
            continuity_gap_p50=("continuity_gap", "median"),
            cascade_risk_p50=("justice_weighted_cascade_risk", "median"),
            cascade_risk_p95=("justice_weighted_cascade_risk", lambda x: np.quantile(x, 0.95)),
        )
        .reset_index()
        .sort_values("cascade_risk_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize cascade diagnostics by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_dependency_pressure=("dependency_pressure", "mean"),
            mean_containment_capacity=("containment_capacity", "mean"),
            mean_governance_response=("governance_response_capacity", "mean"),
            mean_propagation=("propagation_likelihood", "mean"),
            mean_cascade_amplification=("cascade_amplification", "mean"),
            mean_continuity=("essential_function_continuity", "mean"),
            mean_continuity_gap=("continuity_gap", "mean"),
            mean_cascade_risk=("justice_weighted_cascade_risk", "mean"),
        )
        .reset_index()
        .sort_values("mean_cascade_risk", ascending=False)
    )


def main() -> None:
    """Run the full cascading-failure diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "cascading_failures_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "cascading_failures_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "cascading_failures_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "cascading_failures_domain_summary.csv", index=False)

    print("\nCascading-failure diagnostics:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "dependency_pressure",
                "containment_capacity",
                "propagation_likelihood",
                "cascade_amplification",
                "continuity_gap",
                "justice_weighted_cascade_risk",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
