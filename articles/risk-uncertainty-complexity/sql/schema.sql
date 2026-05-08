CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    primary_hazard TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS risk_uncertainty_complexity_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    hazard_probability REAL NOT NULL,
    expected_loss_index REAL NOT NULL,
    probability_uncertainty REAL NOT NULL,
    loss_uncertainty REAL NOT NULL,
    dependency_density REAL NOT NULL,
    feedback_strength REAL NOT NULL,
    threshold_sensitivity REAL NOT NULL,
    adaptive_behavior REAL NOT NULL,
    monitoring_capacity REAL NOT NULL,
    redundancy_capacity REAL NOT NULL,
    flexibility_capacity REAL NOT NULL,
    institutional_learning REAL NOT NULL,
    adaptive_governance_capacity REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    criticality_index REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
