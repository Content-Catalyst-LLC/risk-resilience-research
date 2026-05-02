PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS domains (
    domain_key TEXT PRIMARY KEY,
    domain_name TEXT NOT NULL,
    description TEXT,
    priority INTEGER DEFAULT 3
);

CREATE TABLE IF NOT EXISTS articles (
    slug TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('published','planned','drafting','archived')),
    domain_key TEXT NOT NULL,
    priority INTEGER DEFAULT 3,
    source_focus TEXT,
    FOREIGN KEY (domain_key) REFERENCES domains(domain_key)
);

CREATE TABLE IF NOT EXISTS concepts (
    concept_key TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    concept_family TEXT,
    definition_note TEXT
);

CREATE TABLE IF NOT EXISTS hazards (
    hazard_key TEXT PRIMARY KEY,
    hazard_name TEXT NOT NULL,
    hazard_group TEXT,
    typical_systems_affected TEXT
);

CREATE TABLE IF NOT EXISTS systems (
    system_key TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT,
    critical_functions TEXT
);

CREATE TABLE IF NOT EXISTS indicators (
    indicator_key TEXT PRIMARY KEY,
    indicator_name TEXT NOT NULL,
    indicator_family TEXT,
    measurement_note TEXT,
    warning TEXT
);

CREATE TABLE IF NOT EXISTS scenarios (
    scenario_key TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    primary_hazard TEXT,
    linked_systems TEXT,
    analysis_use TEXT
);

CREATE TABLE IF NOT EXISTS sources (
    source_key TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    institution_or_author TEXT,
    year TEXT,
    source_type TEXT,
    url TEXT
);
