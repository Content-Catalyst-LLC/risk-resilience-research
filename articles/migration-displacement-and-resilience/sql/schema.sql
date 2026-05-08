CREATE TABLE IF NOT EXISTS mobility_places (
    place_id TEXT PRIMARY KEY,
    place_name TEXT NOT NULL,
    region TEXT NOT NULL,
    mobility_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS migration_displacement_indicators (
    indicator_id INTEGER PRIMARY KEY,
    place_id TEXT NOT NULL,
    hazard_pressure REAL NOT NULL,
    livelihood_stress REAL NOT NULL,
    conflict_insecurity_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    mobility_resources REAL NOT NULL,
    protection_access REAL NOT NULL,
    migration_network_strength REAL NOT NULL,
    destination_service_capacity REAL NOT NULL,
    host_community_support REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    arrival_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (place_id) REFERENCES mobility_places(place_id)
);

CREATE TABLE IF NOT EXISTS displacement_events (
    event_id INTEGER PRIMARY KEY,
    place_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT,
    displaced_population INTEGER,
    internal_or_cross_border TEXT,
    trigger_note TEXT,
    protection_note TEXT,
    source_note TEXT,
    FOREIGN KEY (place_id) REFERENCES mobility_places(place_id)
);

CREATE TABLE IF NOT EXISTS host_community_services (
    service_id INTEGER PRIMARY KEY,
    place_id TEXT NOT NULL,
    service_type TEXT NOT NULL,
    service_capacity_score REAL,
    host_support_note TEXT,
    service_gap_note TEXT,
    source_note TEXT,
    FOREIGN KEY (place_id) REFERENCES mobility_places(place_id)
);

CREATE TABLE IF NOT EXISTS mobility_protection_pathways (
    pathway_id INTEGER PRIMARY KEY,
    place_id TEXT NOT NULL,
    pathway_type TEXT NOT NULL,
    legal_access_note TEXT,
    transportation_note TEXT,
    documentation_note TEXT,
    safe_route_note TEXT,
    source_note TEXT,
    FOREIGN KEY (place_id) REFERENCES mobility_places(place_id)
);

CREATE TABLE IF NOT EXISTS remittance_network_records (
    record_id INTEGER PRIMARY KEY,
    place_id TEXT NOT NULL,
    network_type TEXT,
    remittance_note TEXT,
    diaspora_support_note TEXT,
    livelihood_support_note TEXT,
    source_note TEXT,
    FOREIGN KEY (place_id) REFERENCES mobility_places(place_id)
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
