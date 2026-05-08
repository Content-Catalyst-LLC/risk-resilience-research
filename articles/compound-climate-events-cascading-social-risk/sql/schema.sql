CREATE TABLE IF NOT EXISTS compound_event_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    event_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS compound_event_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    concurrent_hazard_intensity REAL NOT NULL,
    sequential_hazard_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    infrastructure_fragility REAL NOT NULL,
    health_system_strain REAL NOT NULL,
    food_water_energy_stress REAL NOT NULL,
    governance_readiness REAL NOT NULL,
    cross_sector_dependency REAL NOT NULL,
    recovery_deficit REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    ecological_buffer_condition REAL NOT NULL,
    social_protection_capacity REAL NOT NULL,
    communication_reliability REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES compound_event_systems(system_id)
);

CREATE TABLE IF NOT EXISTS cascade_pathways (
    pathway_id INTEGER PRIMARY KEY,
    source_system_id TEXT NOT NULL,
    initial_hazard TEXT NOT NULL,
    affected_sector TEXT NOT NULL,
    triggered_effect TEXT NOT NULL,
    pathway_strength REAL NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
