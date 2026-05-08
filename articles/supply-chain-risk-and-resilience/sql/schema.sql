CREATE TABLE IF NOT EXISTS supply_items (
    item_id TEXT PRIMARY KEY,
    item_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    supply_context TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supply_chain_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,
    criticality REAL NOT NULL,
    supplier_concentration REAL NOT NULL,
    dependency_intensity REAL NOT NULL,
    logistics_exposure REAL NOT NULL,
    cyber_digital_risk REAL NOT NULL,
    workforce_vulnerability REAL NOT NULL,
    climate_hazard_exposure REAL NOT NULL,
    inventory_buffer REAL NOT NULL,
    substitutability REAL NOT NULL,
    supplier_redundancy REAL NOT NULL,
    modular_production_capacity REAL NOT NULL,
    governance_capacity REAL NOT NULL,
    logistics_flexibility REAL NOT NULL,
    recovery_time_pressure REAL NOT NULL,
    vulnerable_population_exposure REAL NOT NULL,
    essential_service_relevance REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (item_id) REFERENCES supply_items(item_id)
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,
    supplier_name TEXT,
    supplier_tier INTEGER,
    supplier_region TEXT,
    concentration_note TEXT,
    substitution_note TEXT,
    source_note TEXT,
    FOREIGN KEY (item_id) REFERENCES supply_items(item_id)
);

CREATE TABLE IF NOT EXISTS logistics_routes (
    route_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,
    route_name TEXT NOT NULL,
    route_type TEXT,
    chokepoint_note TEXT,
    climate_exposure_note TEXT,
    cyber_dependency_note TEXT,
    source_note TEXT,
    FOREIGN KEY (item_id) REFERENCES supply_items(item_id)
);

CREATE TABLE IF NOT EXISTS inventory_records (
    inventory_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,
    inventory_days REAL,
    storage_note TEXT,
    rotation_note TEXT,
    strategic_reserve_note TEXT,
    source_note TEXT,
    FOREIGN KEY (item_id) REFERENCES supply_items(item_id)
);

CREATE TABLE IF NOT EXISTS disruption_events (
    disruption_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,
    disruption_date TEXT,
    disruption_type TEXT NOT NULL,
    affected_stage TEXT,
    duration_days REAL,
    shortage_note TEXT,
    recovery_note TEXT,
    source_note TEXT,
    FOREIGN KEY (item_id) REFERENCES supply_items(item_id)
);

CREATE TABLE IF NOT EXISTS procurement_records (
    procurement_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,
    buyer_type TEXT,
    contract_type TEXT,
    resilience_requirement_note TEXT,
    supplier_diversity_note TEXT,
    source_note TEXT,
    FOREIGN KEY (item_id) REFERENCES supply_items(item_id)
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
