# Safety & Audit Performance Dashboard (Synthetic IOSA Dataset)

End-to-end **data analytics & BI project** that simulates an airline’s safety / quality audit program based on the IOSA structure.

The project generates a **realistic synthetic dataset** of internal & provider audits, loads it into a **SQLite data mart**, and surfaces KPIs in a **Power BI executive dashboard** with drill-through analysis.

> All data is 100% synthetic. IOSA sections (ORG, FLT, DSP, CAB, MNT, GRH, CGO, SEC) and ISARP numbers are used only as a realistic reference.

---

## 1. Business context

**Scenario:** An airline Quality & Safety department wants to track:

- Volume and distribution of **audit findings**
- **On-time vs overdue** closure performance
- Risk levels by **IOSA discipline** and **station**
- Where to prioritize follow-up actions (high-risk stations, disciplines, or providers)

This project answers those questions with an **interactive Power BI report** backed by a reproducible Python + SQL pipeline.

---

## 2. Tech stack

- **Python** (pandas, numpy) – synthetic data generation
- **SQLite** – lightweight “audit” database
- **SQL** – KPI & sanity-check queries
- **Power BI Desktop** – data model, DAX measures, executive dashboard
- **Git / GitHub** – version control & project sharing

---

## 3. Data model

The synthetic dataset mimics a small airline audit program with:

- `audits` – header for each audit (type, scope, station, dates, department, provider flag)
- `findings` – individual findings per audit, including:
  - severity, category, IOSA discipline, ISARP reference
  - risk index, probability score, repeat flag
  - dates (raised, due, closed), status (Open / Overdue / Closed)
- `calendar` – date dimension for time-series analysis
- `stations` – station code (IATA style: SJO, MEX, LIM, JFK, etc.), country, region
- `departments` – FO, CAB, MX, GO, CGO, SEC, QMS, DSP (Dispatch)
- `iosa_disciplines` – ORG, FLT, DSP, CAB, MNT, GRH, CGO, SEC
- `iosa_isarps.csv` – mapping of **realistic ISARP numbers** (e.g. `ORG 1.1.1`, `FLT 3.2.4`) to disciplines

The final **Power BI model** uses these relationships:

- `audits 1-* findings`
- `calendar 1-* audits` (via start_date)
- `stations 1-* audits`
- `departments 1-* audits`
- `iosa_disciplines 1-* findings`

---

## 4. Key KPIs & DAX measures

Some of the main measures implemented in Power BI:

- **Total Findings**
- **Open or Overdue Findings**
- **On-Time Closure %**  
  ` = DIVIDE([Closed On Time], [Closed Findings])`
- **Average Closure Days (Closed Only)**
- **High-Critical Findings** (severity in High / Critical)
- **Open or Overdue Findings (Flag)** – for quick filtering

These KPIs are used across cards, bar charts, and drill-through tables.

---

## 5. Power BI report pages

### 5.1 Executive Overview

High-level view for management with slicers for **Year**, **IOSA Discipline**, and **Station**.

**Visuals:**

- KPI cards:
  - Total Findings (All)
  - Open or Overdue Findings
  - On-Time Closure % (with target ≥ 80%)
  - Avg Closure Days (Closed Only)
- Top 10 Stations by Findings (bar chart)
- Total Findings by IOSA Discipline (bar chart)
- Total Findings by Month (line chart)

**Use-case:** “Where are we seeing the highest audit risk overall?”

---

### 5.2 Station Detail (Drill-through)

Detailed table of individual findings with fields such as:

- Station, Department, Audit Type
- Finding ID, description, IOSA reference, severity, risk index
- Status, due / closed dates, closed on time flag
- Repeat flag, root cause, responsible owner

**Accessed via drill-through:**

- Right-click a station bar on the Executive Overview →  
  **Drill through → Station Detail**  
- Filters (Year, Discipline, Station) are preserved.

**Use-case:** “Show me all findings for station SJO in 2023 under ORG.”

---

## 6. How to run this project

### 6.1 Requirements

- Python 3.x installed
- Power BI Desktop
- Git (optional, for cloning)

Install Python packages (from the project root):

```bash
pip install pandas numpy

Generate synthetic CSV data in /data
python generate_synthetic_data.py

Load CSVs into audit.db (SQLite)
python load_to_sqlite.py

---

## 7. Skills demonstrated

This project showcases:

- **Data generation & simulation** with Python (`pandas`, `numpy`)
- Designing a small **relational model** (SQLite) for analytics
- Writing **SQL** for data validation & KPI logic
- Building a **Power BI data model** (relationships, dimensions/facts)
- Implementing **DAX measures** for operational KPIs
- Designing **executive dashboards** with drill-through detail
- Applying domain knowledge in **airline safety / IOSA auditing**
- Using **Git & GitHub** for version control and sharing a reproducible project

---

## 8. Possible extensions

Ideas for future improvements:

- Add a **Provider** dimension (ground handling, maintenance, catering) and related KPIs.
- Include **trend analysis** for On-Time Closure % by quarter / year.
- Build a **risk matrix** (probability × severity) and show high-risk clusters.
- Add **RLS (Row-Level Security)** roles in Power BI (e.g., Station Manager vs. HQ).
- Containerise the pipeline (e.g., simple Docker setup) so it can be run anywhere.
- Expose the SQLite DB to other BI tools (Tableau, Excel) for cross-tool comparison.

---

## 9. Contact

If you have any questions, suggestions, or spot an issue, feel free to:

- Open an **issue** in this repository, or  
- Reach out via **LinkedIn** (link in my GitHub profile).




