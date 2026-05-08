CREATE TABLE IF NOT EXISTS sustainable_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    stress_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stress_test_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    baseline_capacity REAL NOT NULL,
    hazard_intensity REAL NOT NULL,
    exposure REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    interdependence_exposure REAL NOT NULL,
    redundancy REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    monitoring_maturity REAL NOT NULL,
    threshold_level REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES sustainable_systems(system_id)
);

CREATE TABLE IF NOT EXISTS stress_scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    hazard_type TEXT,
    severity_note TEXT,
    compound_stress_note TEXT,
    scenario_design_note TEXT,
    source_note TEXT
);

CREATE TABLE IF NOT EXISTS system_dependencies (
    dependency_id INTEGER PRIMARY KEY,
    dependent_system_id TEXT NOT NULL,
    upstream_system_id TEXT,
    dependency_type TEXT,
    dependency_weight REAL,
    cascading_effect_note TEXT,
    source_note TEXT,
    FOREIGN KEY (dependent_system_id) REFERENCES sustainable_systems(system_id)
);

CREATE TABLE IF NOT EXISTS stress_test_runs (
    run_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    scenario_id INTEGER,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT,
    FOREIGN KEY (system_id) REFERENCES sustainable_systems(system_id),
    FOREIGN KEY (scenario_id) REFERENCES stress_scenarios(scenario_id)
);

CREATE TABLE IF NOT EXISTS stress_test_outputs (
    output_id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    stress_load REAL,
    resilience_capacity REAL,
    failure_pressure REAL,
    threshold_proximity REAL,
    service_continuity_gap REAL,
    priority_score REAL,
    diagnostic_priority TEXT,
    FOREIGN KEY (run_id) REFERENCES stress_test_runs(run_id)
);

CREATE TABLE IF NOT EXISTS source_provenance (
    source_id INTEGER PRIMARY KEY,
    source_title TEXT NOT NULL,
    source_url TEXT,
    source_type TEXT,
    source_note TEXT
);
