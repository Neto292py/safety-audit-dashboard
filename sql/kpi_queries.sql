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
