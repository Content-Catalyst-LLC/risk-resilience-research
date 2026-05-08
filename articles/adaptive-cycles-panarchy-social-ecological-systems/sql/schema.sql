CREATE TABLE IF NOT EXISTS systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    scale_level TEXT NOT NULL,
    domain TEXT NOT NULL,
    region TEXT NOT NULL,
    adaptive_phase TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS adaptive_cycle_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id TEXT NOT NULL,
    growth_potential REAL NOT NULL,
    connectedness REAL NOT NULL,
    rigidity REAL NOT NULL,
    resilience_capacity REAL NOT NULL,
    release_pressure REAL NOT NULL,
    reorganization_capacity REAL NOT NULL,
    novelty_potential REAL NOT NULL,
    memory_capacity REAL NOT NULL,
    revolt_pressure REAL NOT NULL,
    cross_scale_dependency REAL NOT NULL,
    inequality_pressure REAL NOT NULL,
    institutional_learning REAL NOT NULL,
    ecological_buffer_condition REAL NOT NULL,
    governance_flexibility REAL NOT NULL,
    system_criticality REAL NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS panarchy_links (
    link_id INTEGER PRIMARY KEY,
    source_system_id TEXT NOT NULL,
    target_system_id TEXT NOT NULL,
    source_scale TEXT NOT NULL,
    target_scale TEXT NOT NULL,
    link_type TEXT NOT NULL,
    interaction_strength REAL NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS scenario_runs (
    run_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT
);
