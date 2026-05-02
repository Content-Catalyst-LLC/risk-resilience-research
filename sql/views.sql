CREATE VIEW IF NOT EXISTS v_article_roadmap AS
SELECT
    a.priority,
    a.status,
    d.domain_name,
    a.title,
    a.slug,
    a.source_focus
FROM articles a
JOIN domains d ON a.domain_key = d.domain_key
ORDER BY a.priority ASC, d.priority ASC, a.title ASC;

CREATE VIEW IF NOT EXISTS v_concept_map AS
SELECT concept_family, concept_name, definition_note
FROM concepts
ORDER BY concept_family ASC, concept_name ASC;

CREATE VIEW IF NOT EXISTS v_hazard_system_map AS
SELECT hazard_group, hazard_name, typical_systems_affected
FROM hazards
ORDER BY hazard_group ASC, hazard_name ASC;

CREATE VIEW IF NOT EXISTS v_indicator_map AS
SELECT indicator_family, indicator_name, measurement_note, warning
FROM indicators
ORDER BY indicator_family ASC, indicator_name ASC;

CREATE VIEW IF NOT EXISTS v_scenario_matrix AS
SELECT scenario_name, primary_hazard, linked_systems, analysis_use
FROM scenarios
ORDER BY primary_hazard ASC, scenario_name ASC;

CREATE VIEW IF NOT EXISTS v_source_register AS
SELECT source_type, institution_or_author, title, year, url
FROM sources
ORDER BY source_type ASC, institution_or_author ASC;
