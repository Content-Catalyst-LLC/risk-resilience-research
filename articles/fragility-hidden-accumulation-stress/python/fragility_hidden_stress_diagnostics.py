"""
Advanced fragility and hidden stress accumulation diagnostics.

This workflow models:
- visible performance versus hidden stress
- buffer erosion and deferred maintenance
- institutional drift and normalization of weak signals
- standard erosion and threshold proximity
- adaptation debt
- ecological support erosion
- social strain and trust erosion
- monitoring and response capacity
- resilience margin
- justice-weighted fragility
- scenario-based stress reduction and margin restoration
- Monte Carlo uncertainty around fragility classification

The sample data are illustrative. Replace them with documented infrastructure,
public-health, ecological, institutional, and social indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/fragility-hidden-accumulation-stress")
DATA_FILE = BASE_DIR / "data" / "fragility_hidden_stress_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for reducing hidden stress and rebuilding resilience margin."""

    name: str
    stress_reduction: float
    buffer_restoration: float
    maintenance_reduction: float
    drift_reduction: float
    signal_denormalization: float
    standards_restoration: float
    threshold_reduction: float
    adaptation_debt_reduction: float
    ecological_restoration: float
    social_strain_reduction: float
    trust_repair: float
    monitoring_gain: float
    response_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "monitoring_and_signal_repair": Scenario("monitoring_and_signal_repair", 0.08, 0.08, 0.08, 0.14, 0.24, 0.14, 0.06, 0.10, 0.04, 0.08, 0.12, 0.24, 0.12),
    "maintenance_and_buffer_restoration": Scenario("maintenance_and_buffer_restoration", 0.08, 0.24, 0.24, 0.08, 0.10, 0.12, 0.10, 0.10, 0.14, 0.08, 0.08, 0.10, 0.16),
    "anti_drift_governance": Scenario("anti_drift_governance", 0.10, 0.14, 0.16, 0.24, 0.22, 0.24, 0.12, 0.20, 0.12, 0.14, 0.18, 0.20, 0.22),
    "justice_centered_stress_relief": Scenario("justice_centered_stress_relief", 0.16, 0.14, 0.14, 0.16, 0.18, 0.16, 0.12, 0.18, 0.16, 0.24, 0.24, 0.18, 0.22),
    "resilience_margin_rebuild": Scenario("resilience_margin_rebuild", 0.20, 0.26, 0.26, 0.24, 0.24, 0.24, 0.20, 0.24, 0.24, 0.24, 0.24, 0.24, 0.26),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the hidden-fragility panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "visible_performance",
        "stress_accumulation",
        "buffer_erosion",
        "deferred_maintenance",
        "institutional_drift",
        "signal_normalization",
        "standard_erosion",
        "threshold_proximity",
        "adaptation_debt",
        "ecological_support_erosion",
        "social_strain",
        "trust_erosion",
        "monitoring_capacity",
        "response_capacity",
        "justice_pressure",
        "system_criticality",
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
    """Compute hidden stress, fragility, resilience margin, and justice-weighted fragility."""
    scored = df.copy()

    scored["hidden_stress_index"] = (
        0.20 * scored["stress_accumulation"]
        + 0.16 * scored["buffer_erosion"]
        + 0.14 * scored["deferred_maintenance"]
        + 0.13 * scored["adaptation_debt"]
        + 0.12 * scored["ecological_support_erosion"]
        + 0.13 * scored["social_strain"]
        + 0.12 * scored["trust_erosion"]
    )

    scored["drift_index"] = (
        0.34 * scored["institutional_drift"]
        + 0.30 * scored["signal_normalization"]
        + 0.22 * scored["standard_erosion"]
        + 0.14 * (1 - scored["monitoring_capacity"])
    )

    scored["latent_instability"] = (
        0.38 * scored["threshold_proximity"]
        + 0.26 * scored["hidden_stress_index"]
        + 0.20 * scored["drift_index"]
        + 0.16 * scored["system_criticality"]
    )

    scored["resilience_margin"] = (
        0.34 * (1 - scored["buffer_erosion"])
        + 0.24 * scored["monitoring_capacity"]
        + 0.24 * scored["response_capacity"]
        + 0.18 * (1 - scored["threshold_proximity"])
    )

    scored["performance_misalignment"] = np.maximum(
        0,
        scored["visible_performance"] - (1 - scored["hidden_stress_index"]),
    )

    scored["fragility_score"] = (
        0.32 * scored["hidden_stress_index"]
        + 0.24 * scored["drift_index"]
        + 0.24 * scored["latent_instability"]
        + 0.20 * scored["performance_misalignment"]
    ) * (1 + 0.25 * scored["system_criticality"])

    scored["justice_weighted_fragility"] = (
        scored["fragility_score"] * (1 + 0.35 * scored["justice_pressure"])
    )

    scored["resilience_gap"] = np.maximum(
        0,
        scored["justice_weighted_fragility"] - scored["resilience_margin"],
    )

    scored["fragility_band"] = scored["justice_weighted_fragility"].apply(
        lambda x: classify_band(x, low=0.35, high=0.70)
    )

    scored["margin_band"] = scored["resilience_margin"].apply(
        lambda x: classify_band(x, low=0.40, high=0.65)
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["threshold_proximity"] > 0.75,
            scored["drift_index"] > 0.65,
            scored["hidden_stress_index"] > 0.70,
            scored["justice_pressure"] > 0.70,
            scored["performance_misalignment"] > 0.25,
        ],
        [
            "threshold_avoidance_priority",
            "anti_drift_governance_priority",
            "hidden_stress_relief_priority",
            "justice_centered_margin_repair",
            "performance_metric_redesign",
        ],
        default="monitor_and_rebuild_margin",
    )

    return scored.sort_values(
        ["resilience_gap", "justice_weighted_fragility", "latent_instability"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply hidden-stress reduction scenario assumptions and rescore."""
    scenario_df = df.copy()

    scenario_df["stress_accumulation"] = (
        scenario_df["stress_accumulation"] * (1 - scenario.stress_reduction)
    ).clip(0, 1)

    scenario_df["buffer_erosion"] = (
        scenario_df["buffer_erosion"] * (1 - scenario.buffer_restoration)
    ).clip(0, 1)

    scenario_df["deferred_maintenance"] = (
        scenario_df["deferred_maintenance"] * (1 - scenario.maintenance_reduction)
    ).clip(0, 1)

    scenario_df["institutional_drift"] = (
        scenario_df["institutional_drift"] * (1 - scenario.drift_reduction)
    ).clip(0, 1)

    scenario_df["signal_normalization"] = (
        scenario_df["signal_normalization"] * (1 - scenario.signal_denormalization)
    ).clip(0, 1)

    scenario_df["standard_erosion"] = (
        scenario_df["standard_erosion"] * (1 - scenario.standards_restoration)
    ).clip(0, 1)

    scenario_df["threshold_proximity"] = (
        scenario_df["threshold_proximity"] * (1 - scenario.threshold_reduction)
    ).clip(0, 1)

    scenario_df["adaptation_debt"] = (
        scenario_df["adaptation_debt"] * (1 - scenario.adaptation_debt_reduction)
    ).clip(0, 1)

    scenario_df["ecological_support_erosion"] = (
        scenario_df["ecological_support_erosion"] * (1 - scenario.ecological_restoration)
    ).clip(0, 1)

    scenario_df["social_strain"] = (
        scenario_df["social_strain"] * (1 - scenario.social_strain_reduction)
    ).clip(0, 1)

    scenario_df["trust_erosion"] = (
        scenario_df["trust_erosion"] * (1 - scenario.trust_repair)
    ).clip(0, 1)

    scenario_df["monitoring_capacity"] = (
        scenario_df["monitoring_capacity"] + scenario.monitoring_gain
    ).clip(0, 1)

    scenario_df["response_capacity"] = (
        scenario_df["response_capacity"] + scenario.response_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all hidden-stress reduction scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around hidden-fragility scores."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "visible_performance",
        "stress_accumulation",
        "buffer_erosion",
        "deferred_maintenance",
        "institutional_drift",
        "signal_normalization",
        "standard_erosion",
        "threshold_proximity",
        "adaptation_debt",
        "ecological_support_erosion",
        "social_strain",
        "trust_erosion",
        "monitoring_capacity",
        "response_capacity",
        "justice_pressure",
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
                    "hidden_stress_index",
                    "drift_index",
                    "latent_instability",
                    "resilience_margin",
                    "fragility_score",
                    "justice_weighted_fragility",
                    "resilience_gap",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            hidden_stress_p50=("hidden_stress_index", "median"),
            drift_p50=("drift_index", "median"),
            instability_p50=("latent_instability", "median"),
            margin_p50=("resilience_margin", "median"),
            fragility_p50=("justice_weighted_fragility", "median"),
            fragility_p95=("justice_weighted_fragility", lambda x: np.quantile(x, 0.95)),
            resilience_gap_p50=("resilience_gap", "median"),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize fragility diagnostics by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_visible_performance=("visible_performance", "mean"),
            mean_hidden_stress=("hidden_stress_index", "mean"),
            mean_drift=("drift_index", "mean"),
            mean_latent_instability=("latent_instability", "mean"),
            mean_resilience_margin=("resilience_margin", "mean"),
            mean_justice_weighted_fragility=("justice_weighted_fragility", "mean"),
            mean_resilience_gap=("resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )


def main() -> None:
    """Run the full hidden-fragility diagnostic workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "fragility_hidden_stress_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "fragility_hidden_stress_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "fragility_hidden_stress_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "fragility_hidden_stress_domain_summary.csv", index=False)

    print("\nFragility and hidden stress diagnostics:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "visible_performance",
                "hidden_stress_index",
                "drift_index",
                "latent_instability",
                "resilience_margin",
                "justice_weighted_fragility",
                "resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
