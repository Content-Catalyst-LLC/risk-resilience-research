"""
Advanced supply chain risk and resilience diagnostics.

This workflow models criticality, supplier concentration, dependency intensity,
logistics exposure, cyber-digital risk, workforce vulnerability, climate hazard
exposure, buffers, substitutability, redundancy, governance, shortage risk,
continuity gaps, public priority, scenarios, and uncertainty.

The sample data are illustrative. Replace them with documented supplier maps,
trade data, customs data, procurement records, inventory records, port and
logistics data, freight rates, delivery times, supplier audits, workforce
indicators, and service-criticality assessments before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/supply-chain-risk-and-resilience")
DATA_FILE = BASE_DIR / "data" / "supply_chain_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening supply-chain resilience."""

    name: str
    concentration_reduction: float
    dependency_reduction: float
    logistics_exposure_reduction: float
    cyber_risk_reduction: float
    workforce_vulnerability_reduction: float
    climate_exposure_reduction: float
    inventory_gain: float
    substitutability_gain: float
    supplier_redundancy_gain: float
    modularity_gain: float
    governance_gain: float
    logistics_flexibility_gain: float
    recovery_time_reduction: float
    vulnerable_exposure_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "supplier_diversification": Scenario("supplier_diversification", .34, .24, .10, .08, .08, .08, .12, .18, .34, .16, .18, .14, .18, .08),
    "inventory_and_strategic_reserves": Scenario("inventory_and_strategic_reserves", .08, .10, .08, .06, .06, .06, .34, .12, .14, .10, .18, .12, .26, .10),
    "logistics_and_chokepoint_resilience": Scenario("logistics_and_chokepoint_resilience", .10, .12, .34, .12, .10, .20, .16, .14, .18, .16, .20, .34, .20, .12),
    "digital_and_workforce_resilience": Scenario("digital_and_workforce_resilience", .08, .10, .12, .34, .30, .08, .12, .14, .16, .18, .24, .18, .18, .16),
    "integrated_supply_chain_resilience": Scenario("integrated_supply_chain_resilience", .34, .34, .34, .34, .30, .30, .34, .34, .34, .34, .34, .34, .34, .26),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the supply-chain resilience indicator panel."""
    df = pd.read_csv(path)

    required = {
        "item_id",
        "item_name",
        "sector",
        "supply_context",
        "criticality",
        "supplier_concentration",
        "dependency_intensity",
        "logistics_exposure",
        "cyber_digital_risk",
        "workforce_vulnerability",
        "climate_hazard_exposure",
        "inventory_buffer",
        "substitutability",
        "supplier_redundancy",
        "modular_production_capacity",
        "governance_capacity",
        "logistics_flexibility",
        "recovery_time_pressure",
        "vulnerable_population_exposure",
        "essential_service_relevance",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"item_id", "item_name", "sector", "supply_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_supply_chains(df: pd.DataFrame) -> pd.DataFrame:
    """Compute disruption pressure, resilience buffers, shortage risk, and public priority."""
    scored = df.copy()

    scored["disruption_pressure"] = (
        scored["criticality"]
        * (
            0.22 * scored["supplier_concentration"]
            + 0.20 * scored["dependency_intensity"]
            + 0.18 * scored["logistics_exposure"]
            + 0.16 * scored["cyber_digital_risk"]
            + 0.14 * scored["workforce_vulnerability"]
            + 0.10 * scored["climate_hazard_exposure"]
        )
    )

    scored["resilience_buffer_capacity"] = (
        0.22 * scored["inventory_buffer"]
        + 0.20 * scored["substitutability"]
        + 0.20 * scored["supplier_redundancy"]
        + 0.16 * scored["modular_production_capacity"]
        + 0.12 * scored["governance_capacity"]
        + 0.10 * scored["logistics_flexibility"]
    )

    scored["shortage_risk"] = (
        scored["disruption_pressure"]
        * (1 + 0.40 * scored["recovery_time_pressure"])
        * (1 - 0.45 * scored["resilience_buffer_capacity"])
    )

    scored["concentration_adjusted_dependency"] = (
        scored["supplier_concentration"]
        * scored["dependency_intensity"]
        * (1 - scored["substitutability"])
    )

    scored["service_continuity_gap"] = np.maximum(
        0,
        scored["criticality"]
        + scored["shortage_risk"]
        - scored["resilience_buffer_capacity"],
    )

    scored["public_priority_score"] = (
        scored["service_continuity_gap"]
        + 0.30 * scored["criticality"]
        + 0.25 * scored["vulnerable_population_exposure"]
        + 0.25 * scored["essential_service_relevance"]
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["supplier_concentration"] > 0.70,
            scored["logistics_exposure"] > 0.70,
            scored["inventory_buffer"] < 0.35,
            scored["substitutability"] < 0.35,
            scored["supplier_redundancy"] < 0.35,
            scored["service_continuity_gap"] > 0.75,
        ],
        [
            "reduce_supplier_concentration",
            "diversify_logistics_routes_and_chokepoints",
            "increase_inventory_or_strategic_reserves",
            "improve_substitutability_and_standards",
            "expand_supplier_redundancy",
            "close_service_continuity_gap",
        ],
        default="monitor_and_strengthen_supply_chain_resilience",
    )

    return scored.sort_values(
        ["public_priority_score", "service_continuity_gap"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a supply-chain resilience scenario and rescore."""
    x = df.copy()

    x["supplier_concentration"] *= 1 - scenario.concentration_reduction
    x["dependency_intensity"] *= 1 - scenario.dependency_reduction
    x["logistics_exposure"] *= 1 - scenario.logistics_exposure_reduction
    x["cyber_digital_risk"] *= 1 - scenario.cyber_risk_reduction
    x["workforce_vulnerability"] *= 1 - scenario.workforce_vulnerability_reduction
    x["climate_hazard_exposure"] *= 1 - scenario.climate_exposure_reduction
    x["inventory_buffer"] += scenario.inventory_gain
    x["substitutability"] += scenario.substitutability_gain
    x["supplier_redundancy"] += scenario.supplier_redundancy_gain
    x["modular_production_capacity"] += scenario.modularity_gain
    x["governance_capacity"] += scenario.governance_gain
    x["logistics_flexibility"] += scenario.logistics_flexibility_gain
    x["recovery_time_pressure"] *= 1 - scenario.recovery_time_reduction
    x["vulnerable_population_exposure"] *= 1 - scenario.vulnerable_exposure_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"item_id", "item_name", "sector", "supply_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_supply_chains(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all supply-chain resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around shortage-risk and priority scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"item_id", "item_name", "sector", "supply_context"}
    ]

    frames = []
    for draw in range(draws):
        sample = df.copy()
        sample[numeric_cols] = np.clip(
            sample[numeric_cols].to_numpy()
            + rng.normal(0, 0.04, size=(len(sample), len(numeric_cols))),
            0,
            1,
        )
        scored = score_supply_chains(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "item_id",
                    "item_name",
                    "draw",
                    "disruption_pressure",
                    "resilience_buffer_capacity",
                    "shortage_risk",
                    "concentration_adjusted_dependency",
                    "service_continuity_gap",
                    "public_priority_score",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["item_id", "item_name"])
        .agg(
            disruption_pressure_p50=("disruption_pressure", "median"),
            buffer_capacity_p50=("resilience_buffer_capacity", "median"),
            shortage_risk_p50=("shortage_risk", "median"),
            shortage_risk_p95=("shortage_risk", lambda x: np.quantile(x, .95)),
            dependency_p50=("concentration_adjusted_dependency", "median"),
            continuity_gap_p50=("service_continuity_gap", "median"),
            public_priority_p50=("public_priority_score", "median"),
            public_priority_p95=("public_priority_score", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("public_priority_p50", ascending=False)
    )


def main() -> None:
    """Run the full supply-chain risk and resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_supply_chains(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    sector_summary = (
        scored.groupby("sector")
        .agg(
            items=("item_id", "count"),
            mean_disruption_pressure=("disruption_pressure", "mean"),
            mean_buffer_capacity=("resilience_buffer_capacity", "mean"),
            mean_shortage_risk=("shortage_risk", "mean"),
            mean_dependency=("concentration_adjusted_dependency", "mean"),
            mean_continuity_gap=("service_continuity_gap", "mean"),
            mean_public_priority=("public_priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_public_priority", ascending=False)
    )

    context_summary = (
        scored.groupby("supply_context")
        .agg(
            items=("item_id", "count"),
            mean_criticality=("criticality", "mean"),
            mean_supplier_concentration=("supplier_concentration", "mean"),
            mean_logistics_exposure=("logistics_exposure", "mean"),
            mean_buffer_capacity=("resilience_buffer_capacity", "mean"),
            mean_continuity_gap=("service_continuity_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_continuity_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "supply_chain_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "supply_chain_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "supply_chain_resilience_uncertainty.csv", index=False)
    sector_summary.to_csv(OUTPUT_DIR / "supply_chain_sector_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "supply_chain_context_summary.csv", index=False)

    print("\nSupply chain risk and resilience diagnostics:")
    print(
        scored[
            [
                "item_name",
                "sector",
                "supply_context",
                "disruption_pressure",
                "resilience_buffer_capacity",
                "shortage_risk",
                "concentration_adjusted_dependency",
                "service_continuity_gap",
                "public_priority_score",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
