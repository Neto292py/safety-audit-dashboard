# Safety & Audit Performance Dashboard (Synthetic IOSA Dataset)

End-to-end data project that simulates an airline’s **audit & findings tracking** process
and delivers a **Power BI safety dashboard** for management.

All data is **100% synthetic**, but it is structured to resemble a real IOSA audit
environment (disciplines, ISARPs, stations, departments, closure performance, etc.).

---

## 1. Business problem

Airline quality & safety teams run dozens of internal and provider audits every year.
Findings are tracked in spreadsheets or local tools, making it hard to answer basic
questions such as:

- How many findings do we have by **station** and **IOSA discipline**?
- What is our **on-time closure performance** vs target?
- Which **stations / areas** show higher risk (open or overdue, high-critical)?
- How quickly do we close findings on average?

This project builds a repeatable pipeline and dashboard to monitor these questions.

---

## 2. Solution overview

**Tech stack**

- **Python** – generate realistic synthetic IOSA audit & findings data
- **SQLite** – lightweight relational database for analysis & SQL checks
- **SQL** – KPI and sanity-check queries
- **Power BI** – data model, DAX measures, executive dashboard & drill-through
- **Git** – version control for all project assets

**High-level flow**

1. `generate_synthetic_data.py`  
   - Creates synthetic tables: stations, departments, calendar, audits, findings.  
   - Uses a reference file of real IOSA sections and ISARP codes (`data/iosa_isarps.csv`) to
     assign realistic `standard_ref` values (e.g. `ORG 1.1.1`, `FLT 3.2.4`).

2. `load_to_sqlite.py`  
   - Loads the CSV files into a local `audit.db` SQLite database.  
   - Tables: `stations`, `departments`, `calendar`, `audits`, `findings`, `iosa_disciplines`.

3. `sql/core_queries.sql`  
   - Basic data quality checks (row counts, findings by severity, etc.).

4. `sql/kpi_queries.sql`  
   - SQL versions of the main KPIs (total findings, open/overdue, on-time closure, etc.).

5. `Safety_Audit_Dashboard.pbix`  
   - Power BI model + measures + report pages:
     - **Executive Overview**
     - **Station Detail** (drill-through)

---

## 3. Data model

Key tables:

- **stations** – station_code, station_name, country, region  
- **departments** – department_id, department_code (FO, CAB, MX, GRH, CGO, QMS, DSP…), name  
- **calendar** – one row per day, with year, month, year_month, week, etc.  
- **iosa_disciplines** – discipline_code (ORG, FLT, DSP, CAB, MNT, CGO, GRH, SEC), discipline_name  
- **audits** – audit_id, audit_type (Internal IOSA, Station Audit, Provider Audit…), department_id, station_code, start_date, end_date, status  
- **findings** – finding_id, audit_id, severity, risk_index, category, iosadiscipline_code,
  `standard_ref` (ISARP), description, status, date_raised, due_date, date_closed,
  closed_on_time, repeat_flag, root_cause, responsible_owner, probability_score

Relationships in Power BI:

- stations 1─* audits 1─* findings  
- departments 1─* audits  
- iosa_disciplines 1─* findings  
- calendar 1─* findings (via `date_raised`)

---

## 4. Power BI measures (examples)

Core measures in the **findings** table (DAX):

- `Total Findings`  
- `Open or Overdue Findings`  
- `Closed Findings`  
- `High-Critical Findings` (severity in {"High","Critical"})  
- `Closed On Time`  
- `On-Time Closure % = DIVIDE([Closed On Time], [Closed Findings])`  
- `Average Closure Days` (datediff between `date_raised` and `date_closed`)

These measures are reused across all visuals and match SQL checks in
`sql/kpi_queries.sql`.

---

## 5. Report pages

### 5.1 Executive Overview

**Filters**

- Year (from calendar)
- IOSA Discipline
- Station

**KPIs**

- Total Findings (All)
- Open or Overdue Findings
- On-Time Closure % (target ≥ 80%)
- Average Closure Days (Closed Only)

**Visuals**

- Top 10 stations by findings
- Total findings by IOSA discipline
- Total findings by month (for selected year)

This page answers: *“Where are we seeing more findings and how is closure performance
evolving over time?”*

### 5.2 Station Detail (drill-through)

Detailed table of findings including:

- Station, Department, Audit Type
- Finding ID, description, IOSA ref, severity, risk index
- Status, due/closed dates, closed on time flag
- Repeat flag, root cause, responsible owner

Accessed via **drill-through** from the Executive Overview:

- Right-click a station bar → **Drill through → Station Detail**  
- Filters (year, discipline, station) are preserved.

---

## 6. How to run this project

1. **Clone the repo / download the folder**.
2. Install Python dependencies (pandas, numpy, etc.).
3. From the project root, run:

   ```bash
   python generate_synthetic_data.py
   python load_to_sqlite.py

4. Open Safety_Audit_Dashboard.pbix in Power BI Desktop.
5. Click Refresh to pull the latest CSV data.