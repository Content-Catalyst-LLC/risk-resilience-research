-- Risk & Resilience article schema scaffold
-- Supports hazard, exposure, vulnerability, capacity, resilience, justice, and recovery indicators.

CREATE TABLE IF NOT EXISTS systems (
    system_id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS risk_resilience_indicators (
    indicator_id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    hazard_pressure REAL NOT NULL,
    exposure REAL NOT NULL,
    vulnerability REAL NOT NULL,
    protective_capacity REAL NOT NULL,
    robustness REAL NOT NULL,
    redundancy REAL NOT NULL,
    adaptive_capacity REAL NOT NULL,
    recovery_capacity REAL NOT NULL,
    transformation_capacity REAL NOT NULL,
    justice_legitimacy REAL NOT NULL,
    baseline_function REAL NOT NULL,
    minimum_function_after_shock REAL NOT NULL,
    recovery_days INTEGER NOT NULL,
    source_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems(system_id)
);

CREATE TABLE IF NOT EXISTS scoring_runs (
    run_id INTEGER PRIMARY KEY,
    run_label TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    method_note TEXT NOT NULL
);
