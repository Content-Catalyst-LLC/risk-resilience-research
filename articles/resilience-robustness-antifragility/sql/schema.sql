CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS system_response_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    stress_intensity REAL NOT NULL,
    stress_variability REAL NOT NULL,
    system_criticality REAL NOT NULL,
    robustness_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    redundancy_capacity REAL NOT NULL,
    modularity_capacity REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    learning_capacity REAL NOT NULL,
    experimentation_capacity REAL NOT NULL,
    optionality_capacity REAL NOT NULL,
    failure_containment REAL NOT NULL,
    harm_bounding_capacity REAL NOT NULL,
    justice_safeguard_capacity REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
