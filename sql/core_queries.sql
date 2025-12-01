-- 1) List all tables in the database
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

-- 2) Row counts per table (quick sanity check)
SELECT 'audits'          AS table_name, COUNT(*) AS row_count FROM audits
UNION ALL
SELECT 'calendar',       COUNT(*) FROM calendar
UNION ALL
SELECT 'departments',    COUNT(*) FROM departments
UNION ALL
SELECT 'findings',       COUNT(*) FROM findings
UNION ALL
SELECT 'iosa_disciplines', COUNT(*) FROM iosa_disciplines
UNION ALL
SELECT 'stations',       COUNT(*) FROM stations;

-- 3) Total findings and high/critical findings
SELECT
    COUNT(*) AS total_findings,
    SUM(CASE WHEN severity IN ('High', 'Critical') THEN 1 ELSE 0 END) AS high_critical_findings
FROM findings;

-- 4) Findings by severity
SELECT
    severity,
    COUNT(*) AS findings_count
FROM findings
GROUP BY severity
ORDER BY findings_count DESC;

-- 5) Sample of findings (first 20) to inspect structure
SELECT
    finding_id,
    audit_id,
    severity,
    iosa_discipline_code,
    station_code,
    department_id,
    date_raised,
    due_date,
    date_closed,
    status,
    closed_on_time,
    risk_index
FROM findings
ORDER BY finding_id
LIMIT 20;
