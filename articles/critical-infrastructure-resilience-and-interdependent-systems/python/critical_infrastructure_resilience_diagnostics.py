"""
Advanced critical infrastructure resilience and interdependence diagnostics.

This workflow models:
- infrastructure criticality
- hazard exposure
- asset fragility
- cyber-physical risk
- redundancy
- maintenance capacity
- governance capacity
- recovery capacity
- backup capacity
- workforce readiness
- social vulnerability
- service demand under stress
- dependency matrices
- failure pressure
- interdependence exposure
- resilience capacity
- cascading infrastructure risk
- service-continuity gaps
- recovery-priority scoring
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented infrastructure
asset inventories, dependency maps, outage data, maintenance records,
cyber incident records, restoration timelines, climate hazards, and
service-population data before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/critical-infrastructure-resilience-and-interdependent-systems")
DATA_FILE = BASE_DIR / "data" / "critical_infrastructure_resilience_panel.csv"
DEPENDENCY_FILE = BASE_DIR / "data" / "infrastructure_dependency_matrix.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening infrastructure resilience."""

    name: str
    hazard_reduction: float
    asset_fragility_reduction: float
    cyber_risk_reduction: float
    redundancy_gain: float
    maintenance_gain: float
    governance_gain: float
    recovery_gain: float
    backup_gain: float
    workforce_gain: float
    service_demand_reduction: float
    social_vulnerability_reduction: float
    dependency_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "dependency_mapping_and_redundancy": Scenario("dependency_mapping_and_redundancy", .04, .08, .08, .34, .16, .22, .18, .32, .14, .08, .08, .22),
    "maintenance_and_asset_management": Scenario("maintenance_and_asset_management", .06, .30, .08, .14, .34, .20, .20, .18, .20, .08, .10, .08),
    "cyber_physical_resilience": Scenario("cyber_physical_resilience", .04, .08, .34, .18, .16, .30, .22, .20, .28, .06, .08, .12),
    "continuity_and_recovery_capacity": Scenario("continuity_and_recovery_capacity", .06, .12, .12, .22, .20, .24, .34, .30, .30, .24, .12, .14),
    "integrated_infrastructure_resilience": Scenario("integrated_infrastructure_resilience", .22, .34, .34, .34, .34, .34, .34, .34, .34, .28, .30, .30),
}


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and validate the infrastructure system panel and dependency matrix."""
    systems = pd.read_csv(DATA_FILE)
    dependencies = pd.read_csv(DEPENDENCY_FILE, index_col=0)

    required = {
        "system_id",
        "system_name",
        "sector",
        "region",
        "criticality",
        "hazard_exposure",
        "asset_fragility",
        "cyber_physical_risk",
        "redundancy",
        "maintenance_capacity",
        "governance_capacity",
        "recovery_capacity",
        "backup_capacity",
        "workforce_readiness",
        "service_demand_under_stress",
        "social_vulnerability",
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
        if col not in {"system_id", "system_name", "sector", "region"}
    ]

    for col in numeric_cols:
        if ((systems[col] < 0) | (systems[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    if ((dependencies < 0) | (dependencies > 1)).to_numpy().any():
        raise ValueError("Dependency matrix values must be scaled between 0 and 1.")

    return systems, dependencies


def score_systems(systems: pd.DataFrame, dependencies: pd.DataFrame) -> pd.DataFrame:
    """Compute failure pressure, interdependence exposure, cascading risk, and service gaps."""
    scored = systems.copy()

    scored["failure_pressure"] = (
        scored["criticality"]
        * scored["hazard_exposure"]
        * scored["asset_fragility"]
        * (1 + 0.35 * scored["cyber_physical_risk"])
    )

    failure_vector = scored["failure_pressure"].to_numpy()
    dependency_matrix = dependencies.to_numpy()

    scored["interdependence_exposure"] = dependency_matrix.dot(failure_vector)

    scored["resilience_capacity"] = (
        0.22 * scored["redundancy"]
        + 0.20 * scored["maintenance_capacity"]
        + 0.18 * scored["governance_capacity"]
        + 0.18 * scored["recovery_capacity"]
        + 0.12 * scored["backup_capacity"]
        + 0.10 * scored["workforce_readiness"]
    )

    scored["cascading_infrastructure_risk"] = (
        (scored["failure_pressure"] + scored["interdependence_exposure"])
        * (1 + 0.30 * scored["social_vulnerability"])
        * (1 - 0.45 * scored["resilience_capacity"])
    )

    scored["service_continuity_gap"] = np.maximum(
        0,
        scored["service_demand_under_stress"] - scored["resilience_capacity"],
    )

    scored["recovery_priority_score"] = (
        scored["cascading_infrastructure_risk"]
        + 0.35 * scored["service_continuity_gap"]
        + 0.25 * scored["criticality"]
        + 0.20 * scored["social_vulnerability"]
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["interdependence_exposure"] > 0.55,
            scored["cyber_physical_risk"] > 0.65,
            scored["maintenance_capacity"] < 0.42,
            scored["redundancy"] < 0.42,
            scored["governance_capacity"] < 0.42,
            scored["service_continuity_gap"] > 0.35,
        ],
        [
            "map_dependencies_and_reduce_cascading_exposure",
            "strengthen_cyber_physical_resilience",
            "restore_maintenance_and_asset_management",
            "build_redundancy_and_backup_capacity",
            "strengthen_governance_and_accountability",
            "close_service_continuity_gap",
        ],
        default="monitor_and_strengthen_infrastructure_resilience",
    )

    return scored.sort_values(
        ["recovery_priority_score", "cascading_infrastructure_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(
    systems: pd.DataFrame,
    dependencies: pd.DataFrame,
    scenario: Scenario,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply a resilience scenario to systems and dependencies."""
    x = systems.copy()
    dep = dependencies.copy()

    x["hazard_exposure"] *= 1 - scenario.hazard_reduction
    x["asset_fragility"] *= 1 - scenario.asset_fragility_reduction
    x["cyber_physical_risk"] *= 1 - scenario.cyber_risk_reduction
    x["redundancy"] += scenario.redundancy_gain
    x["maintenance_capacity"] += scenario.maintenance_gain
    x["governance_capacity"] += scenario.governance_gain
    x["recovery_capacity"] += scenario.recovery_gain
    x["backup_capacity"] += scenario.backup_gain
    x["workforce_readiness"] += scenario.workforce_gain
    x["service_demand_under_stress"] *= 1 - scenario.service_demand_reduction
    x["social_vulnerability"] *= 1 - scenario.social_vulnerability_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "sector", "region"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    dep = (dep * (1 - scenario.dependency_reduction)).clip(0, 1)

    return x, dep


def run_scenarios(systems: pd.DataFrame, dependencies: pd.DataFrame) -> pd.DataFrame:
    """Run all infrastructure resilience scenarios."""
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
    """Estimate uncertainty around cascading-risk and service-gap scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in systems.columns
        if col not in {"system_id", "system_name", "sector", "region"}
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
                    "failure_pressure",
                    "interdependence_exposure",
                    "resilience_capacity",
                    "cascading_infrastructure_risk",
                    "service_continuity_gap",
                    "recovery_priority_score",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            failure_pressure_p50=("failure_pressure", "median"),
            interdependence_exposure_p50=("interdependence_exposure", "median"),
            resilience_capacity_p50=("resilience_capacity", "median"),
            cascading_risk_p50=("cascading_infrastructure_risk", "median"),
            cascading_risk_p95=("cascading_infrastructure_risk", lambda x: np.quantile(x, .95)),
            service_gap_p50=("service_continuity_gap", "median"),
            recovery_priority_p50=("recovery_priority_score", "median"),
            recovery_priority_p95=("recovery_priority_score", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("recovery_priority_p50", ascending=False)
    )


def main() -> None:
    """Run the full critical infrastructure resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    systems, dependencies = load_data()
    scored = score_systems(systems, dependencies)
    scenarios = run_scenarios(systems, dependencies)
    uncertainty = monte_carlo_uncertainty(systems, dependencies)

    sector_summary = (
        scored.groupby("sector")
        .agg(
            systems=("system_id", "count"),
            mean_failure_pressure=("failure_pressure", "mean"),
            mean_interdependence_exposure=("interdependence_exposure", "mean"),
            mean_resilience_capacity=("resilience_capacity", "mean"),
            mean_cascading_risk=("cascading_infrastructure_risk", "mean"),
            mean_service_gap=("service_continuity_gap", "mean"),
            mean_recovery_priority=("recovery_priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_recovery_priority", ascending=False)
    )

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_failure_pressure=("failure_pressure", "mean"),
            mean_interdependence_exposure=("interdependence_exposure", "mean"),
            mean_resilience_capacity=("resilience_capacity", "mean"),
            mean_cascading_risk=("cascading_infrastructure_risk", "mean"),
            mean_service_gap=("service_continuity_gap", "mean"),
            mean_recovery_priority=("recovery_priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_recovery_priority", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "critical_infrastructure_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "critical_infrastructure_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "critical_infrastructure_resilience_uncertainty.csv", index=False)
    sector_summary.to_csv(OUTPUT_DIR / "critical_infrastructure_sector_summary.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "critical_infrastructure_region_summary.csv", index=False)

    print("\nCritical infrastructure resilience and interdependence diagnostics:")
    print(
        scored[
            [
                "system_name",
                "sector",
                "failure_pressure",
                "interdependence_exposure",
                "resilience_capacity",
                "cascading_infrastructure_risk",
                "service_continuity_gap",
                "recovery_priority_score",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
