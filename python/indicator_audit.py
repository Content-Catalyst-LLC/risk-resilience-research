#!/usr/bin/env python3
from __future__ import annotations
import argparse, sqlite3
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--db", required=True)
parser.add_argument("--output", default="outputs/indicator-audit.md")
args = parser.parse_args()

conn = sqlite3.connect(args.db)
conn.row_factory = sqlite3.Row
rows = list(conn.execute("SELECT * FROM v_indicator_map;"))
conn.close()

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", encoding="utf-8") as f:
    f.write("# Resilience Indicator Audit\n\n")
    for row in rows:
        f.write(f"## {row['indicator_name']}\n\n")
        f.write(f"- Family: {row['indicator_family']}\n")
        f.write(f"- Measurement note: {row['measurement_note']}\n")
        f.write(f"- Warning: {row['warning']}\n\n")

print(f"Exported {len(rows)} indicator audit records to {out}")
