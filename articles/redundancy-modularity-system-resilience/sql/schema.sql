CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS redundancy_modularity_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    primary_failure_pressure REAL NOT NULL,
    redundancy_capacity REAL NOT NULL,
    modularity_capacity REAL NOT NULL,
    backup_diversity REAL NOT NULL,
    pathway_diversity REAL NOT NULL,
    spare_capacity REAL NOT NULL,
    coupling_intensity REAL NOT NULL,
    dependency_concentration REAL NOT NULL,
    containment_strength REAL NOT NULL,
    restoration_capacity REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    governance_coordination REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    system_criticality REAL NOT NULL,
    efficiency_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS redundancy_assets (
    asset_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    redundancy_type TEXT NOT NULL,
    substitute_for TEXT,
    readiness_level REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS modular_segments (
    segment_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    segment_name TEXT NOT NULL,
    containment_boundary TEXT,
    failure_isolation_score REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
