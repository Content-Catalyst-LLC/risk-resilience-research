CREATE TABLE IF NOT EXISTS food_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    region TEXT NOT NULL,
    food_system_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS food_system_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    production_stress REAL NOT NULL,
    water_stress REAL NOT NULL,
    ecological_degradation REAL NOT NULL,
    logistics_fragility REAL NOT NULL,
    input_dependency REAL NOT NULL,
    price_volatility REAL NOT NULL,
    household_vulnerability REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    social_protection_capacity REAL NOT NULL,
    nutritional_adequacy REAL NOT NULL,
    food_system_diversity REAL NOT NULL,
    ecological_buffer_condition REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    market_access_reliability REAL NOT NULL,
    storage_capacity REAL NOT NULL,
    trade_dependency REAL NOT NULL,
    cross_sector_linkage REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES food_systems(system_id)
);

CREATE TABLE IF NOT EXISTS price_shocks (
    shock_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    commodity TEXT NOT NULL,
    price_change_percent REAL,
    shock_date TEXT,
    driver_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES food_systems(system_id)
);

CREATE TABLE IF NOT EXISTS supply_disruptions (
    disruption_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    disruption_type TEXT NOT NULL,
    affected_node TEXT,
    duration_days INTEGER,
    consequence_note TEXT,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES food_systems(system_id)
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
