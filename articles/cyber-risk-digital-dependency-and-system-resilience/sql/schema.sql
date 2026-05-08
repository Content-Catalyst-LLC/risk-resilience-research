CREATE TABLE IF NOT EXISTS digital_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    service_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cyber_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    digital_criticality REAL NOT NULL,
    threat_pressure REAL NOT NULL,
    technical_vulnerability_exposure REAL NOT NULL,
    dependency_concentration REAL NOT NULL,
    identity_access_weakness REAL NOT NULL,
    vendor_supply_chain_exposure REAL NOT NULL,
    operational_technology_exposure REAL NOT NULL,
    data_integrity_risk REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    backup_redundancy_capacity REAL NOT NULL,
    monitoring_maturity REAL NOT NULL,
    logging_maturity REAL NOT NULL,
    incident_exercise_maturity REAL NOT NULL,
    user_vulnerability REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS digital_dependencies (
    dependency_id INTEGER PRIMARY KEY,
    dependent_system_id TEXT NOT NULL,
    upstream_system_id TEXT NOT NULL,
    dependency_weight REAL NOT NULL,
    dependency_type TEXT,
    dependency_note TEXT,
    source_note TEXT,
    FOREIGN KEY (dependent_system_id) REFERENCES digital_systems(system_id),
    FOREIGN KEY (upstream_system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    vendor_name TEXT,
    service_type TEXT,
    access_level TEXT,
    concentration_note TEXT,
    continuity_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS identity_controls (
    identity_control_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    mfa_coverage REAL,
    privileged_access_management_score REAL,
    least_privilege_score REAL,
    identity_lifecycle_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS vulnerability_records (
    vulnerability_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    vulnerability_type TEXT,
    severity_score REAL,
    exposure_note TEXT,
    remediation_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS cyber_incidents (
    incident_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_date TEXT,
    incident_type TEXT,
    affected_function TEXT,
    duration_hours REAL,
    data_integrity_note TEXT,
    recovery_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS recovery_tests (
    recovery_test_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    test_date TEXT,
    recovery_time_hours REAL,
    backup_integrity_score REAL,
    continuity_gap_note TEXT,
    lessons_learned_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES digital_systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);

CREATE TABLE IF NOT EXISTS source_provenance (
    source_id INTEGER PRIMARY KEY,
    source_title TEXT NOT NULL,
    source_url TEXT,
    source_type TEXT,
    source_note TEXT
);
