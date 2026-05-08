CREATE TABLE IF NOT EXISTS fiscal_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    fiscal_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS debt_service_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    debt_service_burden REAL NOT NULL,
    revenue_capacity REAL NOT NULL,
    interest_rate_pressure REAL,
    currency_risk REAL,
    rollover_pressure REAL,
    creditor_concentration REAL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fiscal_systems(system_id)
);

CREATE TABLE IF NOT EXISTS public_resilience_spending (
    spending_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    essential_service_spending REAL NOT NULL,
    public_investment REAL NOT NULL,
    maintenance_capacity REAL NOT NULL,
    adaptation_drr_spending REAL NOT NULL,
    social_protection_capacity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    local_government_capacity REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fiscal_systems(system_id)
);

CREATE TABLE IF NOT EXISTS austerity_records (
    austerity_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    essential_service_cuts REAL NOT NULL,
    public_investment_cuts REAL NOT NULL,
    maintenance_deferral REAL NOT NULL,
    adaptation_deferral REAL NOT NULL,
    social_protection_cuts REAL NOT NULL,
    public_workforce_stress REAL NOT NULL,
    policy_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fiscal_systems(system_id)
);

CREATE TABLE IF NOT EXISTS resilience_risk_indicators (
    risk_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    social_vulnerability REAL NOT NULL,
    hazard_exposure REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    prior_deferred_risk REAL NOT NULL,
    outcome_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES fiscal_systems(system_id)
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
