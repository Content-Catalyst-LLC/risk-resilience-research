CREATE TABLE IF NOT EXISTS public_health_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    health_risk_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public_health_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    health_hazard_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    social_health_vulnerability REAL NOT NULL,
    surveillance_capacity REAL NOT NULL,
    prevention_capacity REAL NOT NULL,
    essential_service_continuity REAL NOT NULL,
    workforce_capacity REAL NOT NULL,
    supply_chain_reliability REAL NOT NULL,
    public_trust REAL NOT NULL,
    communication_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    essential_service_demand REAL NOT NULL,
    repeated_health_disruption_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES public_health_systems(system_id)
);

CREATE TABLE IF NOT EXISTS health_events (
    event_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT,
    severity REAL,
    affected_population INTEGER,
    service_disruption_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES public_health_systems(system_id)
);

CREATE TABLE IF NOT EXISTS service_continuity_records (
    record_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    service_type TEXT NOT NULL,
    continuity_score REAL,
    workforce_note TEXT,
    supply_chain_note TEXT,
    access_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES public_health_systems(system_id)
);

CREATE TABLE IF NOT EXISTS workforce_supply_chain_records (
    record_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    workforce_capacity_score REAL,
    supply_chain_reliability_score REAL,
    procurement_note TEXT,
    staffing_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES public_health_systems(system_id)
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
