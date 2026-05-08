CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS response_pathway_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    disruption_severity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    recovery_speed REAL NOT NULL,
    essential_function_restoration REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    learning_capacity REAL NOT NULL,
    ecological_buffer_capacity REAL NOT NULL,
    social_protection_capacity REAL NOT NULL,
    transformation_readiness REAL NOT NULL,
    structural_unsustainability REAL NOT NULL,
    justice_pressure REAL NOT NULL,
    maladaptation_risk REAL NOT NULL,
    residual_risk REAL NOT NULL,
    public_legitimacy REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
