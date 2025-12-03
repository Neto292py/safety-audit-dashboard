-- =========================================================
-- KPI QUERIES FOR SAFETY & AUDIT PERFORMANCE DASHBOARD
-- These queries are for analysis / validation and to mirror
-- later in Power BI measures.
-- =========================================================

-- 1) Findings by status and severity
--    Basic distribution of findings.
SELECT
    status,
    severity,
    COUNT(*) AS findings_count
FROM findings
GROUP BY
    status,
    severity
ORDER BY
    status,
    findings_count DESC;

-- 2) Average closure days (closed findings only)
--    Measures how long it takes to close findings.
SELECT
    AVG(julianday(date_closed) - julianday(date_raised)) AS avg_closure_days
FROM findings
WHERE status = 'Closed'
  AND date_closed IS NOT NULL
  AND date_raised IS NOT NULL;

-- 3) On-time closure rate (closed findings only)
--    Percentage of closed findings that were closed on or before due date.
SELECT
    COUNT(*) AS closed_findings,
    SUM(
        CASE
            WHEN closed_on_time IN (1, '1', 'True', 'true') THEN 1
            ELSE 0
        END
    ) AS closed_on_time_count,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN closed_on_time IN (1, '1', 'True', 'true') THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        1
    ) AS pct_closed_on_time
FROM findings
WHERE status = 'Closed';


-- 4) Findings by station (with high/critical count)
SELECT
    a.station_code,
    s.station_name,
    s.country,
    COUNT(*) AS total_findings,
    SUM(CASE WHEN f.severity IN ('High', 'Critical') THEN 1 ELSE 0 END) AS high_critical_findings
FROM findings AS f
JOIN audits AS a
    ON a.audit_id = f.audit_id
LEFT JOIN stations AS s
    ON s.station_code = a.station_code
GROUP BY
    a.station_code,
    s.station_name,
    s.country
ORDER BY
    total_findings DESC;


-- 5) On-time closure rate by station (closed findings only)
SELECT
    a.station_code,
    s.station_name,
    COUNT(*) AS closed_findings,
    SUM(
        CASE
            WHEN f.closed_on_time IN (1, '1', 'True', 'true') THEN 1
            ELSE 0
        END
    ) AS closed_on_time_count,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN f.closed_on_time IN (1, '1', 'True', 'true') THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        1
    ) AS pct_closed_on_time
FROM findings AS f
JOIN audits AS a
    ON a.audit_id = f.audit_id
LEFT JOIN stations AS s
    ON s.station_code = a.station_code
WHERE f.status = 'Closed'
GROUP BY
    a.station_code,
    s.station_name
ORDER BY
    pct_closed_on_time DESC;


-- 6) Findings by IOSA discipline
--    Shows which disciplines generate more findings overall.
SELECT
    f.iosa_discipline_code,
    d.discipline_name,
    COUNT(*) AS findings_count
FROM findings AS f
LEFT JOIN iosa_disciplines AS d
    ON f.iosa_discipline_code = d.discipline_code
GROUP BY
    f.iosa_discipline_code,
    d.discipline_name
ORDER BY
    findings_count DESC;


-- 7) Average closure days by IOSA discipline (closed findings only)
--    Helps see where processes are slower to close issues.
SELECT
    f.iosa_discipline_code,
    d.discipline_name,
    AVG(julianday(f.date_closed) - julianday(f.date_raised)) AS avg_closure_days
FROM findings AS f
LEFT JOIN iosa_disciplines AS d
    ON f.iosa_discipline_code = d.discipline_code
WHERE f.status = 'Closed'
  AND f.date_closed IS NOT NULL
  AND f.date_raised IS NOT NULL
GROUP BY
    f.iosa_discipline_code,
    d.discipline_name
ORDER BY
    avg_closure_days DESC;


-- 8) Average risk index by station
SELECT
    a.station_code,
    s.station_name,
    s.country,
    ROUND(AVG(f.risk_index), 2) AS avg_risk_index,
    COUNT(*) AS total_findings
FROM findings AS f
JOIN audits AS a
    ON a.audit_id = f.audit_id
LEFT JOIN stations AS s
    ON s.station_code = a.station_code
GROUP BY
    a.station_code,
    s.station_name,
    s.country
ORDER BY
    avg_risk_index DESC;

