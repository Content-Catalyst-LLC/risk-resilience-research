CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS threshold_tipping_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    stress_load REAL NOT NULL,
    stress_rate REAL NOT NULL,
    resilience_margin REAL NOT NULL,
    buffer_capacity REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    feedback_destabilization REAL NOT NULL,
    threshold_proximity REAL NOT NULL,
    interdependency_density REAL NOT NULL,
    cascade_exposure REAL NOT NULL,
    governance_readiness REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    justice_pressure REAL NOT NULL,
    system_criticality REAL NOT NULL,
    regime_shift_reversibility REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
