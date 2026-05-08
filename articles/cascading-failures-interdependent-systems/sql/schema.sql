CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cascading_failure_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    initiating_shock_severity REAL NOT NULL,
    dependency_density REAL NOT NULL,
    hidden_coupling REAL NOT NULL,
    critical_node_exposure REAL NOT NULL,
    backup_capacity REAL NOT NULL,
    modularity_capacity REAL NOT NULL,
    cross_sector_coordination REAL NOT NULL,
    restoration_speed REAL NOT NULL,
    redundancy_capacity REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    governance_readiness REAL NOT NULL,
    system_criticality REAL NOT NULL,
    cascade_exposure REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    public_trust REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS dependency_edges (
    edge_id INTEGER PRIMARY KEY,
    source_system_id TEXT NOT NULL,
    target_system_id TEXT NOT NULL,
    dependency_type TEXT NOT NULL,
    dependency_strength REAL NOT NULL,
    substitute_available INTEGER DEFAULT 0,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
