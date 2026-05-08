CREATE TABLE IF NOT EXISTS nature_based_solution_projects (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    region TEXT NOT NULL,
    solution_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS nature_based_solution_indicators (
    indicator_id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    ecosystem_condition REAL NOT NULL,
    biodiversity_benefit REAL NOT NULL,
    ecological_connectivity REAL NOT NULL,
    intervention_quality REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    maintenance_capacity REAL NOT NULL,
    hazard_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    social_legitimacy REAL NOT NULL,
    livelihood_benefit REAL NOT NULL,
    displacement_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (project_id) REFERENCES nature_based_solution_projects(project_id)
);

CREATE TABLE IF NOT EXISTS maintenance_records (
    maintenance_id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    maintenance_date TEXT,
    maintenance_type TEXT NOT NULL,
    maintenance_status TEXT,
    budget_note TEXT,
    ecological_note TEXT,
    source_note TEXT,
    FOREIGN KEY (project_id) REFERENCES nature_based_solution_projects(project_id)
);

CREATE TABLE IF NOT EXISTS governance_records (
    governance_id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    community_participation_note TEXT,
    rights_protection_note TEXT,
    grievance_mechanism_note TEXT,
    monitoring_note TEXT,
    source_note TEXT,
    FOREIGN KEY (project_id) REFERENCES nature_based_solution_projects(project_id)
);

CREATE TABLE IF NOT EXISTS hazard_exposure_records (
    hazard_id INTEGER PRIMARY KEY,
    project_id TEXT NOT NULL,
    hazard_type TEXT NOT NULL,
    exposure_measure REAL,
    vulnerability_note TEXT,
    source_note TEXT,
    FOREIGN KEY (project_id) REFERENCES nature_based_solution_projects(project_id)
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
