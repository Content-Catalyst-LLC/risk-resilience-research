CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hidden_fragility_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    visible_performance REAL NOT NULL,
    stress_accumulation REAL NOT NULL,
    buffer_erosion REAL NOT NULL,
    deferred_maintenance REAL NOT NULL,
    institutional_drift REAL NOT NULL,
    signal_normalization REAL NOT NULL,
    standard_erosion REAL NOT NULL,
    threshold_proximity REAL NOT NULL,
    adaptation_debt REAL NOT NULL,
    ecological_support_erosion REAL NOT NULL,
    social_strain REAL NOT NULL,
    trust_erosion REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    response_capacity REAL NOT NULL,
    justice_pressure REAL NOT NULL,
    system_criticality REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
