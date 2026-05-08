CREATE TABLE IF NOT EXISTS fragile_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    fragility_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conflict_fragility_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    conflict_intensity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    service_continuity REAL NOT NULL,
    institutional_legitimacy REAL NOT NULL,
    administrative_reach REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    displacement_pressure REAL NOT NULL,
    livelihood_stress REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    essential_service_demand REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    institutional_exclusion REAL NOT NULL,
    public_trust REAL NOT NULL,
    repeated_disruption_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fragile_systems(system_id)
);

CREATE TABLE IF NOT EXISTS conflict_events (
    event_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT,
    intensity REAL,
    affected_population INTEGER,
    displacement_note TEXT,
    service_disruption_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fragile_systems(system_id)
);

CREATE TABLE IF NOT EXISTS service_continuity_records (
    record_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    service_type TEXT NOT NULL,
    continuity_score REAL,
    disruption_note TEXT,
    responsible_actor TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fragile_systems(system_id)
);

CREATE TABLE IF NOT EXISTS governance_recovery_records (
    recovery_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    program_name TEXT NOT NULL,
    governance_function TEXT,
    coverage_note TEXT,
    legitimacy_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fragile_systems(system_id)
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
