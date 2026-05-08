"""
Advanced cyber risk, digital dependency, and system-resilience diagnostics.

This workflow models:
- digital criticality
- threat pressure
- technical vulnerability exposure
- dependency concentration
- identity and access weakness
- vendor and software supply-chain exposure
- operational-technology exposure
- data-integrity risk
- recovery capacity
- governance capacity
- backup and redundancy capacity
- monitoring maturity
- logging maturity
- incident-exercise maturity
- user vulnerability
- digital dependency matrices
- cyber disruption pressure
- cyber resilience capacity
- systemic cyber risk
- cascading dependency exposure
- service-continuity gaps
- recovery-priority scoring
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented asset inventories,
vulnerability data, identity logs, vendor maps, incident records, outage data,
backup tests, recovery-time measurements, service-criticality assessments,
and community-impact data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/cyber-risk-digital-dependency-and-system-resilience")
DATA_FILE = BASE_DIR / "data" / "cyber_dependency_resilience_panel.csv"
DEPENDENCY_FILE = BASE_DIR / "data" / "digital_dependency_matrix.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening systemic cyber resilience."""

    name: str
    threat_reduction: float
    vulnerability_reduction: float
    dependency_reduction: float
    identity_weakness_reduction: float
    vendor_exposure_reduction: float
    ot_exposure_reduction: float
    data_integrity_reduction: float
    recovery_gain: float
    governance_gain: float
    backup_gain: float
    monitoring_gain: float
    logging_gain: float
    exercise_gain: float
    user_vulnerability_reduction: float
    matrix_dependency_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "identity_and_access_resilience": Scenario("identity_and_access_resilience", .08, .10, .10, .34, .12, .06, .10, .14, .20, .18, .18, .18, .18, .08, .10),
    "vendor_and_dependency_governance": Scenario("vendor_and_dependency_governance", .08, .12, .28, .16, .34, .08, .12, .16, .28, .18, .18, .20, .20, .10, .30),
    "backup_recovery_and_continuity": Scenario("backup_recovery_and_continuity", .06, .10, .10, .12, .12, .10, .12, .34, .22, .34, .20, .22, .30, .12, .12),
    "ot_and_data_integrity_protection": Scenario("ot_and_data_integrity_protection", .10, .16, .10, .12, .12, .34, .34, .18, .22, .18, .24, .24, .20, .10, .12),
    "integrated_systemic_cyber_resilience": Scenario("integrated_systemic_cyber_resilience", .30, .34, .30, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .28, .34),
}


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and validate the cyber system panel and dependency matrix."""
    systems = pd.read_csv(DATA_FILE)
    dependencies = pd.read_csv(DEPENDENCY_FILE, index_col=0)

    required = {
        "system_id",
        "system_name",
        "sector",
        "service_context",
        "digital_criticality",
        "threat_pressure",
        "technical_vulnerability_exposure",
        "dependency_concentration",
        "identity_access_weakness",
        "vendor_supply_chain_exposure",
        "operational_technology_exposure",
        "data_integrity_risk",
        "recovery_capacity",
        "governance_capacity",
        "backup_redundancy_capacity",
        "monitoring_maturity",
        "logging_maturity",
        "incident_exercise_maturity",
        "user_vulnerability",
    }

    missing = required.difference(systems.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    system_ids = list(systems["system_id"])
    if list(dependencies.index) != system_ids:
        raise ValueError("Dependency matrix rows must match system_id order.")
    if list(dependencies.columns) != system_ids:
        raise ValueError("Dependency matrix columns must match system_id order.")

    numeric_cols = [
        col for col in systems.columns
        if col not in {"system_id", "system_name", "sector", "service_context"}
    ]

    for col in numeric_cols:
        if ((systems[col] < 0) | (systems[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    if ((dependencies < 0) | (dependencies > 1)).to_numpy().any():
        raise ValueError("Dependency matrix values must be scaled between 0 and 1.")

    return systems, dependencies


def score_systems(systems: pd.DataFrame, dependencies: pd.DataFrame) -> pd.DataFrame:
    """Compute cyber disruption pressure, systemic risk, cascading exposure, and continuity gaps."""
    scored = systems.copy()

    scored["cyber_disruption_pressure"] = (
        scored["digital_criticality"]
        * (
            0.18 * scored["threat_pressure"]
            + 0.16 * scored["technical_vulnerability_exposure"]
            + 0.15 * scored["dependency_concentration"]
            + 0.15 * scored["identity_access_weakness"]
            + 0.14 * scored["vendor_supply_chain_exposure"]
            + 0.12 * scored["operational_technology_exposure"]
            + 0.10 * scored["data_integrity_risk"]
        )
    )

    scored["cyber_resilience_capacity"] = (
        0.20 * scored["recovery_capacity"]
        + 0.18 * scored["governance_capacity"]
        + 0.17 * scored["backup_redundancy_capacity"]
        + 0.16 * scored["monitoring_maturity"]
        + 0.14 * scored["logging_maturity"]
        + 0.15 * scored["incident_exercise_maturity"]
    )

    scored["systemic_cyber_risk"] = (
        scored["cyber_disruption_pressure"]
        * (1 + 0.35 * scored["dependency_concentration"])
        * (1 + 0.30 * scored["user_vulnerability"])
        * (1 - 0.45 * scored["cyber_resilience_capacity"])
    )

    risk_vector = scored["systemic_cyber_risk"].to_numpy()
    dependency_matrix = dependencies.to_numpy()

    scored["cascading_dependency_exposure"] = dependency_matrix.dot(risk_vector)

    scored["service_continuity_gap"] = np.maximum(
        0,
        scored["digital_criticality"]
        + scored["systemic_cyber_risk"]
        + 0.50 * scored["cascading_dependency_exposure"]
        - scored["cyber_resilience_capacity"],
    )

    scored["recovery_priority_score"] = (
        scored["service_continuity_gap"]
        + 0.30 * scored["digital_criticality"]
        + 0.25 * scored["user_vulnerability"]
        + 0.25 * scored["cascading_dependency_exposure"]
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["identity_access_weakness"] > 0.65,
            scored["vendor_supply_chain_exposure"] > 0.65,
            scored["backup_redundancy_capacity"] < 0.40,
            scored["governance_capacity"] < 0.40,
            scored["cascading_dependency_exposure"] > 0.45,
            scored["service_continuity_gap"] > 0.85,
        ],
        [
            "strengthen_identity_and_access_controls",
            "reduce_vendor_and_software_supply_chain_exposure",
            "improve_backups_redundancy_and_recovery",
            "strengthen_cyber_governance_and_accountability",
            "map_and_reduce_cascading_digital_dependencies",
            "close_service_continuity_gap",
        ],
        default="monitor_and_strengthen_systemic_cyber_resilience",
    )

    return scored.sort_values(
        ["recovery_priority_score", "service_continuity_gap"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(
    systems: pd.DataFrame,
    dependencies: pd.DataFrame,
    scenario: Scenario,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply a systemic cyber-resilience scenario to systems and dependencies."""
    x = systems.copy()
    dep = dependencies.copy()

    x["threat_pressure"] *= 1 - scenario.threat_reduction
    x["technical_vulnerability_exposure"] *= 1 - scenario.vulnerability_reduction
    x["dependency_concentration"] *= 1 - scenario.dependency_reduction
    x["identity_access_weakness"] *= 1 - scenario.identity_weakness_reduction
    x["vendor_supply_chain_exposure"] *= 1 - scenario.vendor_exposure_reduction
    x["operational_technology_exposure"] *= 1 - scenario.ot_exposure_reduction
    x["data_integrity_risk"] *= 1 - scenario.data_integrity_reduction
    x["recovery_capacity"] += scenario.recovery_gain
    x["governance_capacity"] += scenario.governance_gain
    x["backup_redundancy_capacity"] += scenario.backup_gain
    x["monitoring_maturity"] += scenario.monitoring_gain
    x["logging_maturity"] += scenario.logging_gain
    x["incident_exercise_maturity"] += scenario.exercise_gain
    x["user_vulnerability"] *= 1 - scenario.user_vulnerability_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "sector", "service_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    dep = (dep * (1 - scenario.matrix_dependency_reduction)).clip(0, 1)

    return x, dep


def run_scenarios(systems: pd.DataFrame, dependencies: pd.DataFrame) -> pd.DataFrame:
    """Run all cyber-resilience scenarios."""
    outputs = []
    for scenario in SCENARIOS.values():
        scenario_systems, scenario_dependencies = apply_scenario(systems, dependencies, scenario)
        scored = score_systems(scenario_systems, scenario_dependencies)
        scored["scenario"] = scenario.name
        outputs.append(scored)
    return pd.concat(outputs, ignore_index=True)


def monte_carlo_uncertainty(
    systems: pd.DataFrame,
    dependencies: pd.DataFrame,
    draws: int = 2000,
    seed: int = 42,
) -> pd.DataFrame:
    """Estimate uncertainty around systemic cyber risk and continuity gaps."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in systems.columns
        if col not in {"system_id", "system_name", "sector", "service_context"}
    ]

    frames = []
    for draw in range(draws):
        sample = systems.copy()
        sample[numeric_cols] = np.clip(
            sample[numeric_cols].to_numpy()
            + rng.normal(0, 0.04, size=(len(sample), len(numeric_cols))),
            0,
            1,
        )

        dep_sample = pd.DataFrame(
            np.clip(
                dependencies.to_numpy()
                + rng.normal(0, 0.03, size=dependencies.shape),
                0,
                1,
            ),
            index=dependencies.index,
            columns=dependencies.columns,
        )
        np.fill_diagonal(dep_sample.values, 0)

        scored = score_systems(sample, dep_sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "system_id",
                    "system_name",
                    "draw",
                    "cyber_disruption_pressure",
                    "cyber_resilience_capacity",
                    "systemic_cyber_risk",
                    "cascading_dependency_exposure",
                    "service_continuity_gap",
                    "recovery_priority_score",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            disruption_pressure_p50=("cyber_disruption_pressure", "median"),
            resilience_capacity_p50=("cyber_resilience_capacity", "median"),
            systemic_risk_p50=("systemic_cyber_risk", "median"),
            systemic_risk_p95=("systemic_cyber_risk", lambda x: np.quantile(x, .95)),
            cascading_exposure_p50=("cascading_dependency_exposure", "median"),
            continuity_gap_p50=("service_continuity_gap", "median"),
            recovery_priority_p50=("recovery_priority_score", "median"),
            recovery_priority_p95=("recovery_priority_score", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("recovery_priority_p50", ascending=False)
    )


def main() -> None:
    """Run the full cyber risk, digital dependency, and system-resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    systems, dependencies = load_data()
    scored = score_systems(systems, dependencies)
    scenarios = run_scenarios(systems, dependencies)
    uncertainty = monte_carlo_uncertainty(systems, dependencies)

    sector_summary = (
        scored.groupby("sector")
        .agg(
            systems=("system_id", "count"),
            mean_disruption_pressure=("cyber_disruption_pressure", "mean"),
            mean_resilience_capacity=("cyber_resilience_capacity", "mean"),
            mean_systemic_risk=("systemic_cyber_risk", "mean"),
            mean_cascading_exposure=("cascading_dependency_exposure", "mean"),
            mean_continuity_gap=("service_continuity_gap", "mean"),
            mean_recovery_priority=("recovery_priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_recovery_priority", ascending=False)
    )

    context_summary = (
        scored.groupby("service_context")
        .agg(
            systems=("system_id", "count"),
            mean_criticality=("digital_criticality", "mean"),
            mean_identity_weakness=("identity_access_weakness", "mean"),
            mean_vendor_exposure=("vendor_supply_chain_exposure", "mean"),
            mean_resilience_capacity=("cyber_resilience_capacity", "mean"),
            mean_continuity_gap=("service_continuity_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_continuity_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "cyber_dependency_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "cyber_dependency_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "cyber_dependency_resilience_uncertainty.csv", index=False)
    sector_summary.to_csv(OUTPUT_DIR / "cyber_dependency_sector_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "cyber_dependency_context_summary.csv", index=False)

    print("\nCyber risk, digital dependency, and system-resilience diagnostics:")
    print(
        scored[
            [
                "system_name",
                "sector",
                "service_context",
                "cyber_disruption_pressure",
                "cyber_resilience_capacity",
                "systemic_cyber_risk",
                "cascading_dependency_exposure",
                "service_continuity_gap",
                "recovery_priority_score",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
