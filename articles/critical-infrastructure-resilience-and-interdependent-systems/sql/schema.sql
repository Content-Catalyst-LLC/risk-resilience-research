CREATE TABLE IF NOT EXISTS infrastructure_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    region TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS infrastructure_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    criticality REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    asset_fragility REAL NOT NULL,
    cyber_physical_risk REAL NOT NULL,
    redundancy REAL NOT NULL,
    maintenance_capacity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    backup_capacity REAL NOT NULL,
    workforce_readiness REAL NOT NULL,
    service_demand_under_stress REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES infrastructure_systems(system_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_dependencies (
    dependency_id INTEGER PRIMARY KEY,
    dependent_system_id TEXT NOT NULL,
    upstream_system_id TEXT NOT NULL,
    dependency_weight REAL NOT NULL,
    dependency_type TEXT,
    dependency_note TEXT,
    source_note TEXT,
    FOREIGN KEY (dependent_system_id) REFERENCES infrastructure_systems(system_id),
    FOREIGN KEY (upstream_system_id) REFERENCES infrastructure_systems(system_id)
);

CREATE TABLE IF NOT EXISTS infrastructure_outages (
    outage_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    outage_date TEXT,
    outage_type TEXT NOT NULL,
    affected_population INTEGER,
    duration_hours REAL,
    cascading_effect_note TEXT,
    recovery_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES infrastructure_systems(system_id)
);

CREATE TABLE IF NOT EXISTS maintenance_records (
    maintenance_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    asset_class TEXT,
    condition_score REAL,
    deferred_maintenance_note TEXT,
    maintenance_need_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES infrastructure_systems(system_id)
);

CREATE TABLE IF NOT EXISTS cyber_physical_incidents (
    incident_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    incident_date TEXT,
    incident_type TEXT,
    operational_technology_note TEXT,
    service_continuity_note TEXT,
    recovery_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES infrastructure_systems(system_id)
);

CREATE TABLE IF NOT EXISTS service_continuity_records (
    continuity_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    service_function TEXT NOT NULL,
    continuity_score REAL,
    backup_capacity_note TEXT,
    vulnerable_users_note TEXT,
    restoration_priority_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES infrastructure_systems(system_id)
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
