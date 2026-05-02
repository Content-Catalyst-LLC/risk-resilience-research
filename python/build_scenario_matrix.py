#!/usr/bin/env python3
from __future__ import annotations
import argparse, sqlite3
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--db", required=True)
parser.add_argument("--output", default="outputs/scenario-matrix.md")
args = parser.parse_args()

conn = sqlite3.connect(args.db)
conn.row_factory = sqlite3.Row
rows = list(conn.execute("SELECT * FROM v_scenario_matrix;"))
conn.close()

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
cols = ["scenario_name", "primary_hazard", "linked_systems", "analysis_use"]

with out.open("w", encoding="utf-8") as f:
    f.write("# Risk & Resilience Scenario Matrix\n\n")
    f.write("| " + " | ".join(cols) + " |\n")
    f.write("|" + "|".join(["---"] * len(cols)) + "|\n")
    for row in rows:
        f.write("| " + " | ".join(str(row[c] or "").replace("|", "\\|") for c in cols) + " |\n")

print(f"Exported {len(rows)} scenario records to {out}")
