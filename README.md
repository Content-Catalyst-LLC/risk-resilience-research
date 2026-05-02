# Risk & Resilience Research

A companion research infrastructure repository for the Risk & Resilience knowledge series.

This repository supports structured research on systemic risk, resilience concepts, hazards, exposure, vulnerability, adaptive capacity, cascading failures, infrastructure fragility, climate adaptation, resilience indicators, scenario planning, stress testing, article-roadmap planning, source hierarchy, and SQL-backed mapping of risk and resilience research.

It is designed as a clean scholarly infrastructure repository, not a full-stack application. SQL is the backbone. CSV files provide maintainable reference data. Python and R are used only for lightweight exports, audits, indicator summaries, and scenario matrices.

## Repository Structure

- `articles/risk-resilience/` — Article planning notes and pillar support
- `data/` — CSV metadata for domains, articles, concepts, hazards, systems, indicators, scenarios, and sources
- `docs/` — Methodology, source hierarchy, citation style, measurement notes, article template, and licensing notes
- `sql/` — Schema, seed data, and research views
- `python/` — Lightweight export, audit, and scenario utilities
- `r/` — Lightweight resilience indicator summaries
- `notebooks/` — Optional exploratory notebooks
- `outputs/` — Generated roadmaps, maps, and audits

## Quick Start with SQLite

```bash
sqlite3 risk_resilience.db < sql/schema.sql
sqlite3 risk_resilience.db < sql/seed_risk_resilience.sql
sqlite3 risk_resilience.db < sql/views.sql

python3 python/export_article_roadmap.py --db risk_resilience.db --output outputs/article-roadmap.md
python3 python/build_scenario_matrix.py --db risk_resilience.db --output outputs/scenario-matrix.md
python3 python/indicator_audit.py --db risk_resilience.db --output outputs/indicator-audit.md
Rscript r/resilience_indicator_summary.R
```

## License

Code, SQL, and repository infrastructure are released under the MIT License. Original documentation and metadata are covered by `CONTENT_LICENSE.md`. Official source materials remain the property of their respective institutions and should be cited and linked from authoritative sources.
