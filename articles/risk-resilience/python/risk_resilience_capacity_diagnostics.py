"""
Sustainable systems risk and resilience capacity diagnostics.

Synthetic-data workflow for the article:
"What Are Risk and Resilience in Sustainable Systems?"
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


INPUT_FILE = Path("articles/risk-resilience/data/risk_resilience_profiles.csv")
OUTPUT_DIR = Path("articles/risk-resilience/outputs")


def load_profiles(path: Path = INPUT_FILE) -> pd.DataFrame:
    """Load risk and resilience profile data."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    return pd.read_csv(path)


def validate_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Validate index-like fields and recovery days."""
    required = [
        "system_name",
        "system_type",
        "hazard_pressure",
        "exposure",
        "vulnerability",
        "protective_capacity",
        "robustness",
        "redundancy",
        "adaptive_capacity",
        "recovery_capacity",
        "transformation_capacity",
        "justice_legitimacy",
        "baseline_function",
        "minimum_function_after_shock",
        "recovery_days",
    ]

    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    index_columns = [
        column for column in required
        if column not in {"system_name", "system_type", "recovery_days"}
    ]

    for column in index_columns:
        invalid = df[column].lt(0) | df[column].gt(1)
        if invalid.any():
            systems = df.loc[invalid, "system_name"].tolist()
            raise ValueError(f"{column} outside [0, 1] for: {systems}")

    if df["recovery_days"].le(0).any():
        raise ValueError("recovery_days must be positive.")

    return df


def functional_loss_area(row: pd.Series) -> float:
    """Estimate cumulative functional loss using a linear recovery curve."""
    days = np.arange(0, int(row["recovery_days"]) + 1)
    recovery_curve = np.linspace(
        float(row["minimum_function_after_shock"]),
        float(row["baseline_function"]),
        num=len(days),
    )
    gap = float(row["baseline_function"]) - recovery_curve
    return float(np.trapz(gap, days))


def score_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate risk, resilience, justice-adjusted risk, and priority scores."""
    scored = df.copy()

    scored["risk_score"] = (
        scored["hazard_pressure"]
        * scored["exposure"]
        * scored["vulnerability"]
        * (1 - scored["protective_capacity"])
    ).clip(0, 1)

    scored["resilience_capacity"] = (
        0.22 * scored["robustness"]
        + 0.20 * scored["redundancy"]
        + 0.22 * scored["adaptive_capacity"]
        + 0.18 * scored["recovery_capacity"]
        + 0.18 * scored["transformation_capacity"]
    ).clip(0, 1)

    scored["resilience_adjusted_risk"] = (
        scored["risk_score"] / (1 + scored["resilience_capacity"])
    ).clip(0, 1)

    scored["justice_adjusted_risk"] = (
        scored["resilience_adjusted_risk"] * (1 - scored["justice_legitimacy"])
    ).clip(0, 1)

    scored["functional_loss_area"] = scored.apply(functional_loss_area, axis=1)

    scored["priority_score"] = (
        0.35 * scored["resilience_adjusted_risk"]
        + 0.30 * scored["justice_adjusted_risk"]
        + 0.20 * scored["functional_loss_area"].rank(pct=True)
        + 0.15 * (1 - scored["protective_capacity"])
    ).clip(0, 1)

    scored["resilience_gap"] = scored["risk_score"] - scored["resilience_capacity"]

    scored["resilience_gap_class"] = pd.cut(
        scored["resilience_gap"],
        bins=[-np.inf, 0.06, 0.18, 0.30, np.inf],
        labels=[
            "lower_resilience_gap",
            "moderate_resilience_gap",
            "high_resilience_gap",
            "severe_resilience_gap",
        ],
        right=False,
    )

    return scored.sort_values("priority_score", ascending=False)


def summarize_by_system_type(scored: pd.DataFrame) -> pd.DataFrame:
    """Summarize scores by system type."""
    return (
        scored.groupby("system_type")
        .agg(
            systems=("system_name", "count"),
            mean_risk_score=("risk_score", "mean"),
            mean_resilience_capacity=("resilience_capacity", "mean"),
            mean_resilience_adjusted_risk=("resilience_adjusted_risk", "mean"),
            mean_justice_adjusted_risk=("justice_adjusted_risk", "mean"),
            mean_functional_loss_area=("functional_loss_area", "mean"),
            mean_priority_score=("priority_score", "mean"),
        )
        .reset_index()
        .sort_values("mean_priority_score", ascending=False)
    )


def main() -> None:
    """Run the workflow and export outputs."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    profiles = validate_profiles(load_profiles())
    scored = score_profiles(profiles)
    summary = summarize_by_system_type(scored)

    scored.to_csv(OUTPUT_DIR / "risk_resilience_scores.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "risk_resilience_summary.csv", index=False)

    print(scored.round(3).to_string(index=False))
    print("\nSummary:")
    print(summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
