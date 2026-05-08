CREATE TABLE IF NOT EXISTS water_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    water_stress_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS water_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    drought_pressure REAL NOT NULL,
    flood_exposure REAL NOT NULL,
    water_demand_pressure REAL NOT NULL,
    water_availability REAL NOT NULL,
    infrastructure_reliability REAL NOT NULL,
    water_quality REAL NOT NULL,
    ecosystem_buffer_condition REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    social_protection_capacity REAL NOT NULL,
    livelihood_water_dependency REAL NOT NULL,
    critical_service_dependence REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    maintenance_deficit REAL NOT NULL,
    pollution_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES water_systems(system_id)
);

CREATE TABLE IF NOT EXISTS water_hazard_events (
    event_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT,
    severity REAL,
    affected_population INTEGER,
    infrastructure_damage_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES water_systems(system_id)
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
