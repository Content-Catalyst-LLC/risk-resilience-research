"""
Advanced threshold, tipping-point, and system-breakdown diagnostics.

This workflow models:
- stress load and stress rate
- resilience margin and buffer capacity
- threshold proximity
- feedback destabilization
- tipping pressure
- regime shift likelihood
- cascading breakdown potential
- recovery difficulty and reversibility
- governance readiness
- justice-weighted breakdown risk
- scenario-based margin restoration
- Monte Carlo uncertainty around nonlinear breakdown classification

The sample data are illustrative. Replace them with documented climate, ecological,
infrastructure, governance, public-health, and community indicators before applied use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


BASE_DIR = Path("articles/thresholds-tipping-points-system-breakdown")
DATA_FILE = BASE_DIR / "data" / "threshold_tipping_system_panel.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


@dataclass(frozen=True)
class Scenario:
    """Scenario assumptions for reducing tipping pressure and restoring resilience margin."""

    name: str
    stress_reduction: float
    stress_rate_reduction: float
    margin_gain: float
    buffer_gain: float
    monitoring_gain: float
    feedback_stabilization: float
    threshold_retreat: float
    interdependency_reduction: float
    cascade_reduction: float
    governance_gain: float
    recovery_gain: float
    vulnerability_reduction: float
    justice_reduction: float
    reversibility_gain: float


SCENARIOS: Dict[str, Scenario] = {
    "baseline": Scenario("baseline", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00),
    "early_warning_and_monitoring": Scenario("early_warning_and_monitoring", 0.04, 0.06, 0.08, 0.06, 0.26, 0.12, 0.08, 0.04, 0.06, 0.16, 0.08, 0.06, 0.06, 0.08),
    "margin_and_buffer_restoration": Scenario("margin_and_buffer_restoration", 0.08, 0.08, 0.26, 0.28, 0.10, 0.14, 0.16, 0.06, 0.08, 0.12, 0.18, 0.08, 0.08, 0.14),
    "cascade_containment": Scenario("cascade_containment", 0.06, 0.06, 0.14, 0.16, 0.14, 0.18, 0.12, 0.20, 0.28, 0.18, 0.16, 0.10, 0.10, 0.12),
    "justice_centered_threshold_avoidance": Scenario("justice_centered_threshold_avoidance", 0.10, 0.10, 0.18, 0.20, 0.18, 0.18, 0.18, 0.12, 0.14, 0.22, 0.20, 0.24, 0.24, 0.18),
    "resilience_before_breakdown": Scenario("resilience_before_breakdown", 0.18, 0.16, 0.30, 0.30, 0.26, 0.26, 0.24, 0.22, 0.26, 0.26, 0.26, 0.22, 0.22, 0.24),
}


def load_data(path: Path) -> pd.DataFrame:
    """Load and validate the threshold-tipping-point panel."""
    df = pd.read_csv(path)

    required = {
        "system_id",
        "system_name",
        "domain",
        "region",
        "stress_type",
        "stress_load",
        "stress_rate",
        "resilience_margin",
        "buffer_capacity",
        "monitoring_capacity",
        "feedback_destabilization",
        "threshold_proximity",
        "interdependency_density",
        "cascade_exposure",
        "governance_readiness",
        "recovery_capacity",
        "social_vulnerability",
        "justice_pressure",
        "system_criticality",
        "regime_shift_reversibility",
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
    """Compute tipping, regime-shift, cascade, and breakdown-risk diagnostics."""
    scored = df.copy()

    scored["effective_margin"] = (
        0.42 * scored["resilience_margin"]
        + 0.24 * scored["buffer_capacity"]
        + 0.18 * scored["monitoring_capacity"]
        + 0.16 * scored["governance_readiness"]
    )

    scored["threshold_pressure"] = (
        0.34 * scored["stress_load"]
        + 0.22 * scored["stress_rate"]
        + 0.26 * scored["threshold_proximity"]
        + 0.18 * scored["feedback_destabilization"]
    )

    scored["tipping_pressure"] = (
        scored["threshold_pressure"]
        * (1 + 0.35 * scored["feedback_destabilization"])
        * (1 + 0.25 * scored["stress_rate"])
        * (1 - 0.45 * scored["effective_margin"])
    )

    scored["regime_shift_likelihood"] = (
        0.34 * scored["tipping_pressure"]
        + 0.26 * scored["threshold_proximity"]
        + 0.20 * scored["feedback_destabilization"]
        + 0.20 * (1 - scored["regime_shift_reversibility"])
    ).clip(0, 1.5)

    scored["cascade_potential"] = (
        scored["regime_shift_likelihood"]
        * (1 + scored["interdependency_density"])
        * (1 + 0.5 * scored["cascade_exposure"])
        * (1 + 0.35 * scored["system_criticality"])
    )

    scored["recovery_difficulty"] = (
        0.32 * scored["regime_shift_likelihood"]
        + 0.24 * (1 - scored["recovery_capacity"])
        + 0.22 * (1 - scored["regime_shift_reversibility"])
        + 0.22 * scored["social_vulnerability"]
    ).clip(0, 1.5)

    scored["breakdown_risk"] = (
        0.34 * scored["regime_shift_likelihood"]
        + 0.28 * scored["cascade_potential"].clip(0, 1.5)
        + 0.20 * scored["recovery_difficulty"]
        + 0.18 * scored["social_vulnerability"]
    )

    scored["justice_weighted_breakdown_risk"] = (
        scored["breakdown_risk"]
        * (1 + 0.35 * scored["justice_pressure"])
    )

    scored["resilience_gap"] = np.maximum(
        0,
        scored["justice_weighted_breakdown_risk"] - scored["effective_margin"],
    )

    scored["threshold_band"] = scored["threshold_proximity"].apply(
        lambda x: classify_band(x, low=0.40, high=0.70)
    )

    scored["breakdown_band"] = scored["justice_weighted_breakdown_risk"].apply(
        lambda x: classify_band(x, low=0.45, high=0.85)
    )

    scored["diagnostic_priority"] = np.select(
        [
            scored["threshold_proximity"] > 0.80,
            scored["cascade_potential"] > 1.40,
            scored["regime_shift_likelihood"] > 0.75,
            scored["effective_margin"] < 0.45,
            scored["justice_pressure"] > 0.70,
        ],
        [
            "critical_threshold_avoidance",
            "cascade_containment_priority",
            "regime_shift_prevention",
            "resilience_margin_rebuild",
            "justice_centered_breakdown_prevention",
        ],
        default="monitor_and_preserve_margin",
    )

    return scored.sort_values(
        ["resilience_gap", "justice_weighted_breakdown_risk", "cascade_potential"],
        ascending=False,
    ).reset_index(drop=True)


def apply_scenario(df: pd.DataFrame, scenario: Scenario) -> pd.DataFrame:
    """Apply threshold and tipping-risk reduction scenario assumptions."""
    scenario_df = df.copy()

    scenario_df["stress_load"] = (
        scenario_df["stress_load"] * (1 - scenario.stress_reduction)
    ).clip(0, 1)

    scenario_df["stress_rate"] = (
        scenario_df["stress_rate"] * (1 - scenario.stress_rate_reduction)
    ).clip(0, 1)

    scenario_df["resilience_margin"] = (
        scenario_df["resilience_margin"] + scenario.margin_gain
    ).clip(0, 1)

    scenario_df["buffer_capacity"] = (
        scenario_df["buffer_capacity"] + scenario.buffer_gain
    ).clip(0, 1)

    scenario_df["monitoring_capacity"] = (
        scenario_df["monitoring_capacity"] + scenario.monitoring_gain
    ).clip(0, 1)

    scenario_df["feedback_destabilization"] = (
        scenario_df["feedback_destabilization"] * (1 - scenario.feedback_stabilization)
    ).clip(0, 1)

    scenario_df["threshold_proximity"] = (
        scenario_df["threshold_proximity"] * (1 - scenario.threshold_retreat)
    ).clip(0, 1)

    scenario_df["interdependency_density"] = (
        scenario_df["interdependency_density"] * (1 - scenario.interdependency_reduction)
    ).clip(0, 1)

    scenario_df["cascade_exposure"] = (
        scenario_df["cascade_exposure"] * (1 - scenario.cascade_reduction)
    ).clip(0, 1)

    scenario_df["governance_readiness"] = (
        scenario_df["governance_readiness"] + scenario.governance_gain
    ).clip(0, 1)

    scenario_df["recovery_capacity"] = (
        scenario_df["recovery_capacity"] + scenario.recovery_gain
    ).clip(0, 1)

    scenario_df["social_vulnerability"] = (
        scenario_df["social_vulnerability"] * (1 - scenario.vulnerability_reduction)
    ).clip(0, 1)

    scenario_df["justice_pressure"] = (
        scenario_df["justice_pressure"] * (1 - scenario.justice_reduction)
    ).clip(0, 1)

    scenario_df["regime_shift_reversibility"] = (
        scenario_df["regime_shift_reversibility"] + scenario.reversibility_gain
    ).clip(0, 1)

    rescored = score_systems(scenario_df)
    rescored["scenario"] = scenario.name

    return rescored


def run_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    """Run all threshold and tipping-point scenarios."""
    frames = [apply_scenario(df, scenario) for scenario in SCENARIOS.values()]
    return pd.concat(frames, ignore_index=True)


def monte_carlo_uncertainty(
    df: pd.DataFrame,
    draws: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run Monte Carlo uncertainty around threshold and tipping diagnostics."""
    rng = np.random.default_rng(seed)
    records = []

    numeric_cols = [
        "stress_load",
        "stress_rate",
        "resilience_margin",
        "buffer_capacity",
        "monitoring_capacity",
        "feedback_destabilization",
        "threshold_proximity",
        "interdependency_density",
        "cascade_exposure",
        "governance_readiness",
        "recovery_capacity",
        "social_vulnerability",
        "justice_pressure",
        "system_criticality",
        "regime_shift_reversibility",
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
                    "effective_margin",
                    "threshold_pressure",
                    "tipping_pressure",
                    "regime_shift_likelihood",
                    "cascade_potential",
                    "recovery_difficulty",
                    "justice_weighted_breakdown_risk",
                    "resilience_gap",
                ]
            ]
        )

    mc = pd.concat(records, ignore_index=True)

    return (
        mc.groupby(["system_id", "system_name"])
        .agg(
            effective_margin_p50=("effective_margin", "median"),
            tipping_pressure_p50=("tipping_pressure", "median"),
            regime_shift_p50=("regime_shift_likelihood", "median"),
            cascade_p50=("cascade_potential", "median"),
            cascade_p95=("cascade_potential", lambda x: np.quantile(x, 0.95)),
            breakdown_risk_p50=("justice_weighted_breakdown_risk", "median"),
            breakdown_risk_p95=("justice_weighted_breakdown_risk", lambda x: np.quantile(x, 0.95)),
            resilience_gap_p50=("resilience_gap", "median"),
        )
        .reset_index()
        .sort_values("resilience_gap_p50", ascending=False)
    )


def build_domain_summary(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize threshold, tipping, cascade, and breakdown diagnostics by domain."""
    return (
        scored.groupby("domain")
        .agg(
            systems=("system_id", "count"),
            mean_effective_margin=("effective_margin", "mean"),
            mean_threshold_pressure=("threshold_pressure", "mean"),
            mean_tipping_pressure=("tipping_pressure", "mean"),
            mean_regime_shift_likelihood=("regime_shift_likelihood", "mean"),
            mean_cascade_potential=("cascade_potential", "mean"),
            mean_recovery_difficulty=("recovery_difficulty", "mean"),
            mean_breakdown_risk=("justice_weighted_breakdown_risk", "mean"),
            mean_resilience_gap=("resilience_gap", "mean"),
        )
        .reset_index()
        .sort_values("mean_resilience_gap", ascending=False)
    )


def main() -> None:
    """Run the full threshold-tipping-system-breakdown workflow."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw = load_data(DATA_FILE)
    scored = score_systems(raw)
    scenarios = run_scenarios(raw)
    uncertainty = monte_carlo_uncertainty(raw, draws=2000)
    domain_summary = build_domain_summary(scored)

    scored.to_csv(OUTPUT_DIR / "threshold_tipping_system_scores.csv", index=False)
    scenarios.to_csv(OUTPUT_DIR / "threshold_tipping_system_scenarios.csv", index=False)
    uncertainty.to_csv(OUTPUT_DIR / "threshold_tipping_system_uncertainty.csv", index=False)
    domain_summary.to_csv(OUTPUT_DIR / "threshold_tipping_system_domain_summary.csv", index=False)

    print("\nThreshold, tipping point, and breakdown diagnostics:")
    print(
        scored[
            [
                "system_name",
                "domain",
                "stress_type",
                "effective_margin",
                "threshold_proximity",
                "tipping_pressure",
                "regime_shift_likelihood",
                "cascade_potential",
                "justice_weighted_breakdown_risk",
                "resilience_gap",
                "diagnostic_priority",
            ]
        ].round(3).to_string(index=False)
    )

    print("\nDomain summary:")
    print(domain_summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
