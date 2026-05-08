"""
Advanced food system fragility and resilience diagnostics.

This workflow models:
- production stress
- water stress
- ecological degradation
- logistics fragility
- input dependency
- price volatility
- household vulnerability
- inequality pressure
- social protection capacity
- nutritional adequacy
- food system diversity
- ecological buffer condition
- governance capacity
- market access reliability
- storage capacity
- trade dependency
- cross-sector linkage
- food system fragility
- food access vulnerability
- resilience capacity
- cascading food risk
- justice-weighted food risk
- food-resilience gaps
- scenario-based resilience strategies
- Monte Carlo uncertainty around food-risk classification

The sample data are illustrative. Replace them with documented crop, market,
nutrition, food access, logistics, ecological, water, governance, and household data
before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/food-system-fragility-and-resilience")
DATA_FILE = BASE_DIR / "data" / "food_system_fragility_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for strengthening food-system resilience."""

    name: str
    production_stress_reduction: float
    water_stress_reduction: float
    ecological_restoration_gain: float
    logistics_gain: float
    input_dependency_reduction: float
    price_volatility_reduction: float
    household_vulnerability_reduction: float
    inequality_reduction: float
    social_protection_gain: float
    nutritional_gain: float
    diversity_gain: float
    ecological_buffer_gain: float
    governance_gain: float
    market_access_gain: float
    storage_gain: float
    trade_dependency_reduction: float
    cross_sector_linkage_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "climate_resilient_production": Scenario("climate_resilient_production", .24, .20, .18, .06, .10, .08, .06, .06, .08, .10, .16, .18, .12, .08, .10, .06, .06),
    "logistics_storage_continuity": Scenario("logistics_storage_continuity", .06, .06, .06, .30, .10, .18, .08, .08, .10, .08, .08, .08, .14, .22, .30, .10, .18),
    "social_protection_and_nutrition": Scenario("social_protection_and_nutrition", .06, .08, .08, .08, .08, .22, .28, .30, .32, .30, .08, .08, .18, .12, .12, .08, .08),
    "agroecology_and_local_diversity": Scenario("agroecology_and_local_diversity", .18, .18, .30, .10, .24, .10, .12, .14, .16, .18, .34, .32, .18, .12, .16, .18, .12),
    "integrated_food_system_resilience": Scenario("integrated_food_system_resilience", .28, .28, .30, .30, .28, .26, .30, .30, .32, .30, .34, .34, .32, .30, .30, .26, .24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the food system indicator panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "region",
        "food_system_type",
        "production_stress",
        "water_stress",
        "ecological_degradation",
        "logistics_fragility",
        "input_dependency",
        "price_volatility",
        "household_vulnerability",
        "inequality_pressure",
        "social_protection_capacity",
        "nutritional_adequacy",
        "food_system_diversity",
        "ecological_buffer_condition",
        "governance_capacity",
        "market_access_reliability",
        "storage_capacity",
        "trade_dependency",
        "cross_sector_linkage",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "food_system_type"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute food-system fragility, access vulnerability, and resilience-gap scores."""
    scored = df.copy()

    scored["food_system_fragility"] = (
        0.20 * scored["production_stress"]
        + 0.18 * scored["water_stress"]
        + 0.18 * scored["ecological_degradation"]
        + 0.16 * scored["logistics_fragility"]
        + 0.14 * scored["input_dependency"]
        + 0.14 * scored["price_volatility"]
    )

    scored["food_access_vulnerability"] = (
        0.24 * scored["household_vulnerability"]
        + 0.22 * scored["price_volatility"]
        + 0.20 * scored["inequality_pressure"]
        + 0.18 * (1 - scored["social_protection_capacity"])
        + 0.16 * (1 - scored["nutritional_adequacy"])
    )

    scored["resilience_capacity"] = (
        0.20 * scored["food_system_diversity"]
        + 0.18 * scored["ecological_buffer_condition"]
        + 0.18 * scored["social_protection_capacity"]
        + 0.16 * scored["governance_capacity"]
        + 0.14 * scored["market_access_reliability"]
        + 0.14 * scored["storage_capacity"]
    )

    scored["cascading_food_risk"] = (
        (scored["food_system_fragility"] + scored["food_access_vulnerability"])
        * (1 + 0.30 * scored["trade_dependency"])
        * (1 + 0.30 * scored["cross_sector_linkage"])
    )

    scored["justice_weighted_food_risk"] = (
        scored["cascading_food_risk"]
        * (1 + 0.35 * scored["inequality_pressure"])
    )

    scored["food_resilience_gap"] = np.maximum(
        0,
        scored["justice_weighted_food_risk"] - scored["resilience_capacity"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["production_stress"] > 0.72,
            scored["water_stress"] > 0.72,
            scored["ecological_degradation"] > 0.70,
            scored["logistics_fragility"] > 0.70,
            scored["household_vulnerability"] > 0.70,
            scored["food_resilience_gap"] > 1.0,
        ],
        [
            "production_and_climate_resilience",
            "water_secure_food_systems",
            "ecological_restoration_and_soil_health",
            "logistics_storage_and_market_continuity",
            "social_protection_and_food_access",
            "close_food_resilience_gap",
        ],
        default="monitor_and_preserve_food_system_resilience",
    )

    return scored.sort_values(
        ["food_resilience_gap", "justice_weighted_food_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a food-system resilience scenario and rescore."""
    x = df.copy()

    x["production_stress"] *= 1 - scenario.production_stress_reduction
    x["water_stress"] *= 1 - scenario.water_stress_reduction
    x["ecological_degradation"] *= 1 - scenario.ecological_restoration_gain
    x["logistics_fragility"] *= 1 - scenario.logistics_gain
    x["input_dependency"] *= 1 - scenario.input_dependency_reduction
    x["price_volatility"] *= 1 - scenario.price_volatility_reduction
    x["household_vulnerability"] *= 1 - scenario.household_vulnerability_reduction
    x["inequality_pressure"] *= 1 - scenario.inequality_reduction
    x["social_protection_capacity"] += scenario.social_protection_gain
    x["nutritional_adequacy"] += scenario.nutritional_gain
    x["food_system_diversity"] += scenario.diversity_gain
    x["ecological_buffer_condition"] += scenario.ecological_buffer_gain
    x["governance_capacity"] += scenario.governance_gain
    x["market_access_reliability"] += scenario.market_access_gain
    x["storage_capacity"] += scenario.storage_gain
    x["trade_dependency"] *= 1 - scenario.trade_dependency_reduction
    x["cross_sector_linkage"] *= 1 - scenario.cross_sector_linkage_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "food_system_type"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_systems(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all food-system resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around food-system risk and resilience-gap scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "food_system_type"}
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
        scored = score_systems(sample)
        scored["draw"] = draw
        frames.append(
            scored[
                [
                    "system_id",
                    "system_name",
                    "draw",
                    "food_system_fragility",
                    "food_access_vulnerability",
                    "resilience_capacity",
                    "cascading_food_risk",
                    "justice_weighted_food_risk",
                    "food_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            fragility_p50=("food_system_fragility", "median"),
            access_vulnerability_p50=("food_access_vulnerability", "median"),
            resilience_capacity_p50=("resilience_capacity", "median"),
            cascading_risk_p50=("cascading_food_risk", "median"),
            justice_risk_p50=("justice_weighted_food_risk", "median"),
            justice_risk_p95=("justice_weighted_food_risk", lambda x: np.quantile(x, .95)),
            resilience_gap_p50=("food_resilience_gap", "median"),
            resilience_gap_p95=("food_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full food-system fragility and resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_fragility=("food_system_fragility", "mean"),
            mean_access_vulnerability=("food_access_vulnerability", "mean"),
            mean_cascading_risk=("cascading_food_risk", "mean"),
            mean_resilience_capacity=("resilience_capacity", "mean"),
            mean_resilience_gap=("food_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    type_summary = (
        scored.groupby("food_system_type")
        .agg(
            systems=("system_id", "count"),
            mean_production_stress=("production_stress", "mean"),
            mean_water_stress=("water_stress", "mean"),
            mean_fragility=("food_system_fragility", "mean"),
            mean_access_vulnerability=("food_access_vulnerability", "mean"),
            mean_resilience_gap=("food_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "food_system_fragility_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "food_system_fragility_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "food_system_fragility_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "food_system_region_summary.csv", index=False)
    type_summary.to_csv(OUTPUT_DIR / "food_system_type_summary.csv", index=False)

    print("\nFood system fragility and resilience diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "food_system_type",
                "food_system_fragility",
                "food_access_vulnerability",
                "resilience_capacity",
                "cascading_food_risk",
                "justice_weighted_food_risk",
                "food_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
