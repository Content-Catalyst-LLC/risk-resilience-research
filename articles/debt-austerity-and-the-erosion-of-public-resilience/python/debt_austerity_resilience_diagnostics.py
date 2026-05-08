"""
Advanced debt, austerity, and public-resilience diagnostics.

This workflow models:
- debt service burden
- revenue capacity
- essential service spending
- public investment
- maintenance capacity
- adaptation and disaster-risk-reduction spending
- social protection capacity
- governance capacity
- local government capacity
- austerity intensity
- social vulnerability
- hazard exposure
- inequality pressure
- deferred risk
- fiscal resilience risk
- public resilience gaps
- scenario analysis
- Monte Carlo uncertainty

The sample data are illustrative. Replace them with documented fiscal accounts,
debt-service records, public expenditure data, infrastructure maintenance data,
adaptation and DRR spending, social protection records, hazard exposure data,
and social vulnerability indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/debt-austerity-and-the-erosion-of-public-resilience")
DATA_FILE = BASE_DIR / "data" / "debt_austerity_resilience_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for improving fiscal resilience without destructive austerity."""

    name: str
    debt_service_reduction: float
    revenue_capacity_gain: float
    essential_spending_gain: float
    public_investment_gain: float
    maintenance_gain: float
    adaptation_gain: float
    social_protection_gain: float
    governance_gain: float
    local_government_gain: float
    essential_cuts_reduction: float
    investment_cuts_reduction: float
    maintenance_deferral_reduction: float
    adaptation_deferral_reduction: float
    social_protection_cuts_reduction: float
    workforce_stress_reduction: float
    vulnerability_reduction: float
    hazard_exposure_reduction: float
    inequality_reduction: float
    deferred_risk_reduction: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    "debt_relief_and_revenue_reform": Scenario("debt_relief_and_revenue_reform", .34, .30, .12, .14, .12, .14, .16, .16, .14, .16, .18, .18, .18, .18, .16, .10, .08, .18, .12),
    "protect_essential_services": Scenario("protect_essential_services", .12, .14, .34, .14, .16, .14, .28, .18, .18, .34, .16, .16, .16, .30, .24, .22, .08, .22, .14),
    "restore_maintenance_and_adaptation": Scenario("restore_maintenance_and_adaptation", .10, .14, .16, .28, .34, .34, .16, .16, .22, .14, .28, .34, .34, .14, .18, .12, .28, .12, .30),
    "social_protection_and_local_capacity": Scenario("social_protection_and_local_capacity", .10, .18, .18, .16, .18, .16, .34, .22, .34, .20, .18, .18, .18, .34, .24, .30, .10, .30, .18),
    "integrated_fiscal_resilience": Scenario("integrated_fiscal_resilience", .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .34, .30, .34, .34),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the debt-austerity resilience indicator panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "region",
        "fiscal_context",
        "debt_service_burden",
        "revenue_capacity",
        "essential_service_spending",
        "public_investment",
        "maintenance_capacity",
        "adaptation_drr_spending",
        "social_protection_capacity",
        "governance_capacity",
        "local_government_capacity",
        "essential_service_cuts",
        "public_investment_cuts",
        "maintenance_deferral",
        "adaptation_deferral",
        "social_protection_cuts",
        "public_workforce_stress",
        "social_vulnerability",
        "hazard_exposure",
        "inequality_pressure",
        "prior_deferred_risk",
    }

    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "fiscal_context"}
    ]

    for col in numeric_cols:
        if ((df[col] < 0) | (df[col] > 1)).any():
            raise ValueError(f"{col} must be scaled between 0 and 1.")

    return df


def score_systems(df: pd.DataFrame) -> pd.DataFrame:
    """Compute debt pressure, public resilience capacity, austerity intensity, and gaps."""
    scored = df.copy()

    scored["debt_service_pressure"] = (
        scored["debt_service_burden"]
        / (0.20 + scored["revenue_capacity"])
    ).clip(0, 1.5)

    scored["public_resilience_capacity"] = (
        0.18 * scored["essential_service_spending"]
        + 0.16 * scored["public_investment"]
        + 0.15 * scored["maintenance_capacity"]
        + 0.16 * scored["adaptation_drr_spending"]
        + 0.15 * scored["social_protection_capacity"]
        + 0.12 * scored["governance_capacity"]
        + 0.08 * scored["local_government_capacity"]
    )

    scored["austerity_intensity"] = (
        0.20 * scored["essential_service_cuts"]
        + 0.20 * scored["public_investment_cuts"]
        + 0.18 * scored["maintenance_deferral"]
        + 0.18 * scored["adaptation_deferral"]
        + 0.16 * scored["social_protection_cuts"]
        + 0.08 * scored["public_workforce_stress"]
    )

    scored["fiscal_resilience_risk"] = (
        (scored["debt_service_pressure"] + scored["austerity_intensity"])
        * (1 + 0.35 * scored["social_vulnerability"])
        * (1 + 0.30 * scored["hazard_exposure"])
        * (1 + 0.25 * scored["inequality_pressure"])
        * (1 - 0.45 * scored["public_resilience_capacity"])
    )

    scored["deferred_risk_burden"] = (
        scored["prior_deferred_risk"]
        + 0.40 * scored["austerity_intensity"]
        - 0.20 * scored["public_investment"]
        - 0.20 * scored["maintenance_capacity"]
        - 0.20 * scored["adaptation_drr_spending"]
    ).clip(0, 1.5)

    scored["public_resilience_gap"] = np.maximum(
        0,
        scored["fiscal_resilience_risk"]
        + scored["deferred_risk_burden"]
        - scored["public_resilience_capacity"],
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["debt_service_pressure"] > 0.85,
            scored["essential_service_cuts"] > 0.65,
            scored["maintenance_deferral"] > 0.65,
            scored["adaptation_deferral"] > 0.65,
            scored["social_protection_cuts"] > 0.65,
            scored["public_resilience_gap"] > 0.75,
        ],
        [
            "debt_restructuring_or_debt_service_relief",
            "protect_essential_services",
            "restore_maintenance_and_infrastructure_capacity",
            "protect_climate_adaptation_and_drr",
            "protect_social_protection_and_care_systems",
            "close_public_resilience_gap",
        ],
        default="monitor_and_strengthen_fiscal_resilience",
    )

    return scored.sort_values(
        ["public_resilience_gap", "fiscal_resilience_risk"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply a fiscal resilience scenario and rescore."""
    x = df.copy()

    x["debt_service_burden"] *= 1 - scenario.debt_service_reduction
    x["revenue_capacity"] += scenario.revenue_capacity_gain
    x["essential_service_spending"] += scenario.essential_spending_gain
    x["public_investment"] += scenario.public_investment_gain
    x["maintenance_capacity"] += scenario.maintenance_gain
    x["adaptation_drr_spending"] += scenario.adaptation_gain
    x["social_protection_capacity"] += scenario.social_protection_gain
    x["governance_capacity"] += scenario.governance_gain
    x["local_government_capacity"] += scenario.local_government_gain
    x["essential_service_cuts"] *= 1 - scenario.essential_cuts_reduction
    x["public_investment_cuts"] *= 1 - scenario.investment_cuts_reduction
    x["maintenance_deferral"] *= 1 - scenario.maintenance_deferral_reduction
    x["adaptation_deferral"] *= 1 - scenario.adaptation_deferral_reduction
    x["social_protection_cuts"] *= 1 - scenario.social_protection_cuts_reduction
    x["public_workforce_stress"] *= 1 - scenario.workforce_stress_reduction
    x["social_vulnerability"] *= 1 - scenario.vulnerability_reduction
    x["hazard_exposure"] *= 1 - scenario.hazard_exposure_reduction
    x["inequality_pressure"] *= 1 - scenario.inequality_reduction
    x["prior_deferred_risk"] *= 1 - scenario.deferred_risk_reduction

    numeric_cols = [
        col for col in x.columns
        if col not in {"system_id", "system_name", "region", "fiscal_context"}
    ]
    x[numeric_cols] = x[numeric_cols].clip(0, 1)

    scored = score_systems(x)
    scored["scenario"] = scenario.name
    return scored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all debt-austerity fiscal resilience scenarios."""
    return pd.concat([apply_scenario(df, scenario) for scenario in SCENARIOS.values()], ignore_index=True)


def monte_carlo_uncertainty(df: pd.DataFrame, draws: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Estimate uncertainty around fiscal resilience and public resilience gap scores."""
    rng = np.random.default_rng(seed)
    numeric_cols = [
        col for col in df.columns
        if col not in {"system_id", "system_name", "region", "fiscal_context"}
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
                    "debt_service_pressure",
                    "public_resilience_capacity",
                    "austerity_intensity",
                    "fiscal_resilience_risk",
                    "deferred_risk_burden",
                    "public_resilience_gap",
                ]
            ]
        )

    mc = pd.concat(frames, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            debt_pressure_p50=("debt_service_pressure", "median"),
            public_capacity_p50=("public_resilience_capacity", "median"),
            austerity_p50=("austerity_intensity", "median"),
            fiscal_risk_p50=("fiscal_resilience_risk", "median"),
            fiscal_risk_p95=("fiscal_resilience_risk", lambda x: np.quantile(x, .95)),
            deferred_risk_p50=("deferred_risk_burden", "median"),
            resilience_gap_p50=("public_resilience_gap", "median"),
            resilience_gap_p95=("public_resilience_gap", lambda x: np.quantile(x, .95)),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def main() -> None:
    """Run the full debt, austerity, and public-resilience workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw)

    region_summary = (
        scored.groupby("region")
        .agg(
            systems=("system_id", "count"),
            mean_debt_pressure=("debt_service_pressure", "mean"),
            mean_austerity=("austerity_intensity", "mean"),
            mean_public_capacity=("public_resilience_capacity", "mean"),
            mean_fiscal_risk=("fiscal_resilience_risk", "mean"),
            mean_deferred_risk=("deferred_risk_burden", "mean"),
            mean_resilience_gap=("public_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    context_summary = (
        scored.groupby("fiscal_context")
        .agg(
            systems=("system_id", "count"),
            mean_debt_service_burden=("debt_service_burden", "mean"),
            mean_revenue_capacity=("revenue_capacity", "mean"),
            mean_austerity=("austerity_intensity", "mean"),
            mean_public_capacity=("public_resilience_capacity", "mean"),
            mean_resilience_gap=("public_resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )

    scored.to_csv(OUTPUT_DIR / "debt_austerity_resilience_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "debt_austerity_resilience_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "debt_austerity_resilience_uncertainty.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "debt_austerity_region_summary.csv", index=False)
    context_summary.to_csv(OUTPUT_DIR / "debt_austerity_context_summary.csv", index=False)

    print("\nDebt, austerity, and public-resilience diagnostics:")
    print(
        scored[
            [
                "system_name",
                "region",
                "fiscal_context",
                "debt_service_pressure",
                "austerity_intensity",
                "public_resilience_capacity",
                "fiscal_resilience_risk",
                "deferred_risk_burden",
                "public_resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )


if __name__ == "__main__":
    main()
