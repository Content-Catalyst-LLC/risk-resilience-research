#!/usr/bin/env python3
from __future__ import annotations
import argparse, sqlite3
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--db", required=True)
parser.add_argument("--output", default="outputs/article-roadmap.md")
args = parser.parse_args()

conn = sqlite3.connect(args.db)
conn.row_factory = sqlite3.Row
rows = list(conn.execute("SELECT * FROM v_article_roadmap;"))
conn.close()

out = Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
cols = ["priority", "status", "domain_name", "title", "slug", "source_focus"]

with out.open("w", encoding="utf-8") as f:
    f.write("# Risk & Resilience Article Roadmap\n\n")
    f.write("| " + " | ".join(cols) + " |\n")
    f.write("|" + "|".join(["---"] * len(cols)) + "|\n")
    for row in rows:
        f.write("| " + " | ".join(str(row[c] or "").replace("|", "\\|") for c in cols) + " |\n")

print(f"Exported {len(rows)} article records to {out}")
