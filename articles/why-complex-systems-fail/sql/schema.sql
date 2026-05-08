CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS complex_failure_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    dependency_density REAL NOT NULL,
    hidden_coupling REAL NOT NULL,
    feedback_delay REAL NOT NULL,
    signal_visibility REAL NOT NULL,
    buffer_capacity REAL NOT NULL,
    redundancy_capacity REAL NOT NULL,
    modularity_capacity REAL NOT NULL,
    adaptation_debt REAL NOT NULL,
    optimization_pressure REAL NOT NULL,
    maintenance_deficit REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    governance_coordination REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    system_criticality REAL NOT NULL,
    external_stress REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
