CREATE TABLE IF NOT EXISTS communities (
    community_id TEXT PRIMARY KEY,
    community_name TEXT NOT NULL,
    region TEXT NOT NULL,
    risk_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS community_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    community_id TEXT NOT NULL,
    hazard_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    social_vulnerability REAL NOT NULL,
    trust_level REAL NOT NULL,
    local_organizational_capacity REAL NOT NULL,
    mutual_aid_strength REAL NOT NULL,
    communication_access REAL NOT NULL,
    local_knowledge_integration REAL NOT NULL,
    institutional_support REAL NOT NULL,
    participation_quality REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    exclusion_pressure REAL NOT NULL,
    institutional_follow_through REAL NOT NULL,
    broken_promise_pressure REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (community_id) REFERENCES communities(community_id)
);

CREATE TABLE IF NOT EXISTS local_organizations (
    organization_id INTEGER PRIMARY KEY,
    community_id TEXT NOT NULL,
    organization_name TEXT NOT NULL,
    organization_type TEXT,
    trusted_messenger_role TEXT,
    service_or_support_role TEXT,
    source_note TEXT,
    FOREIGN KEY (community_id) REFERENCES communities(community_id)
);

CREATE TABLE IF NOT EXISTS participation_processes (
    process_id INTEGER PRIMARY KEY,
    community_id TEXT NOT NULL,
    process_name TEXT NOT NULL,
    participation_quality_score REAL,
    shared_authority_note TEXT,
    accessibility_note TEXT,
    compensation_note TEXT,
    source_note TEXT,
    FOREIGN KEY (community_id) REFERENCES communities(community_id)
);

CREATE TABLE IF NOT EXISTS hazard_response_records (
    response_id INTEGER PRIMARY KEY,
    community_id TEXT NOT NULL,
    hazard_type TEXT NOT NULL,
    response_date TEXT,
    community_action_note TEXT,
    institutional_support_note TEXT,
    unmet_need_note TEXT,
    source_note TEXT,
    FOREIGN KEY (community_id) REFERENCES communities(community_id)
);

CREATE TABLE IF NOT EXISTS trust_recovery_records (
    record_id INTEGER PRIMARY KEY,
    community_id TEXT NOT NULL,
    institutional_follow_through REAL,
    broken_promise_pressure REAL,
    trust_repair_note TEXT,
    recovery_support_note TEXT,
    source_note TEXT,
    FOREIGN KEY (community_id) REFERENCES communities(community_id)
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
