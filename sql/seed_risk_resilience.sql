PRAGMA foreign_keys = ON;

.mode csv
.import --skip 1 data/domains.csv domains
.import --skip 1 data/articles.csv articles
.import --skip 1 data/concepts.csv concepts
.import --skip 1 data/hazards.csv hazards
.import --skip 1 data/systems.csv systems
.import --skip 1 data/indicators.csv indicators
.import --skip 1 data/scenarios.csv scenarios
.import --skip 1 data/sources.csv sources
