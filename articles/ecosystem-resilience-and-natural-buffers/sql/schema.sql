CREATE TABLE IF NOT EXISTS ecosystem_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    ecosystem_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ecosystem_buffer_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    ecosystem_condition REAL NOT NULL,
    ecological_connectivity REAL NOT NULL,
    functional_biodiversity REAL NOT NULL,
    maintenance_capacity REAL NOT NULL,
    restoration_investment REAL NOT NULL,
    hazard_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    degradation_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES ecosystem_systems(system_id)
);

CREATE TABLE IF NOT EXISTS restoration_projects (
    project_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    project_name TEXT NOT NULL,
    project_type TEXT NOT NULL,
    start_year INTEGER,
    restoration_area_hectares REAL,
    expected_buffer_function TEXT,
    governance_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES ecosystem_systems(system_id)
);

CREATE TABLE IF NOT EXISTS hazard_exposure_records (
    record_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    hazard_type TEXT NOT NULL,
    exposure_measure REAL,
    vulnerability_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES ecosystem_systems(system_id)
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
