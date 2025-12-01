"""
Synthetic IOSA Safety & Audit Dataset Generator
-----------------------------------------------
Generates CSV files for:
- iosa_disciplines
- departments
- stations
- calendar
- audits
- findings

All data is 100% synthetic.
"""

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# -------------------------------------------------------------------
# 0. Setup
# -------------------------------------------------------------------
np.random.seed(42)
# (pandas uses NumPy's RNG; this is enough for reproducibility)

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# "Today" reference for open/overdue logic
TODAY = datetime(2024, 12, 31)
CAPA_GO_LIVE = datetime(2023, 1, 1)

# -------------------------------------------------------------------
# 1. IOSA Disciplines dimension
# -------------------------------------------------------------------
iosa_disciplines = pd.DataFrame({
    "discipline_code": ["ORG", "FLT", "DSP", "CAB", "MNT", "GRH", "CGO", "SEC"],
    "discipline_name": [
        "Organization and Management",
        "Flight Operations",
        "Operational Control and Flight Dispatch",
        "Cabin Operations",
        "Aircraft Engineering and Maintenance",
        "Ground Handling Operations",
        "Cargo Operations",
        "Security Management"
    ]
})

# -------------------------------------------------------------------
# 2. Departments dimension
# -------------------------------------------------------------------
departments = pd.DataFrame({
    "department_id": range(1, 9),
    "department_code": ["FO", "CC", "MX", "GO", "CGO", "SEC", "QMS", "DSP"],
    "department_name": [
        "Flight Operations",
        "Cabin Crew",
        "Maintenance",
        "Ground Operations",
        "Cargo",
        "Security",
        "Quality & Safety Management",
        "Dispatch"
    ]
})

# Mapping department → likely IOSA disciplines (for more realistic data)
dept_to_disciplines = {
    "FO": ["FLT", "DSP", "ORG"],
    "CC": ["CAB", "ORG"],
    "MX": ["MNT", "ORG"],
    "GO": ["GRH", "ORG", "DSP"],
    "CGO": ["CGO", "ORG"],
    "SEC": ["SEC", "ORG"],
    "QMS": ["ORG"],
    "DSP": ["DSP", "FLT", "ORG"]
}

# -------------------------------------------------------------------
# 3. Stations dimension (1 per country, real-like IATA codes)
# -------------------------------------------------------------------
stations_data = [
    ("SJO", "San José",        "Costa Rica",     "Central America"),
    ("MEX", "Mexico City",     "Mexico",         "North America"),
    ("SAL", "San Salvador",    "El Salvador",    "Central America"),
    ("GUA", "Guatemala City",  "Guatemala",      "Central America"),
    ("SAP", "San Pedro Sula",  "Honduras",       "Central America"),
    ("PTY", "Panama City",     "Panama",         "Central America"),
    ("MIA", "Miami",           "United States",  "North America"),
    ("BOG", "Bogotá",          "Colombia",       "South America"),
    ("LIM", "Lima",            "Peru",           "South America"),
    ("SCL", "Santiago",        "Chile",          "South America"),
    ("LAX", "Los Angeles",     "United States",  "North America"),
    ("JFK", "New York",       "United States",    "North America"),
]

stations = pd.DataFrame(
    stations_data,
    columns=["station_code", "station_name", "country", "region"]
)

# -------------------------------------------------------------------
# 4. Calendar dimension
# -------------------------------------------------------------------
date_range = pd.date_range(start="2021-01-01", end="2024-12-31", freq="D")
calendar = pd.DataFrame({"date": date_range})
calendar["day"] = calendar["date"].dt.day
calendar["month"] = calendar["date"].dt.month
calendar["year"] = calendar["date"].dt.year
calendar["week"] = calendar["date"].dt.isocalendar().week.astype(int)
calendar["quarter"] = calendar["date"].dt.quarter
calendar["month_name"] = calendar["date"].dt.month_name()
calendar["year_month"] = calendar["date"].dt.to_period("M").astype(str)

# -------------------------------------------------------------------
# 5. Audits fact table
# -------------------------------------------------------------------
n_audits = 400

audit_types = ["Internal IOSA", "Station Audit", "Provider Audit", "Thematic Audit"]
audit_type_probs = [0.4, 0.25, 0.25, 0.10]

provider_types = ["Ground Handling", "Catering", "Maintenance", "Security", "Cargo"]

start_date_min = datetime(2021, 1, 1)
start_date_max = datetime(2024, 12, 15)
delta_days = (start_date_max - start_date_min).days

audit_rows = []

for audit_id in range(1, n_audits + 1):
    audit_type = np.random.choice(audit_types, p=audit_type_probs)

    station = stations.sample(1).iloc[0]
    dept = departments.sample(1).iloc[0]

    # Random start date
    start = start_date_min + timedelta(days=int(np.random.randint(0, delta_days + 1)))
    duration = int(np.random.randint(2, 6))  # 2–5 days
    end = start + timedelta(days=duration)

    is_provider = audit_type == "Provider Audit"
    provider_type = np.random.choice(provider_types) if is_provider else None

    # Simple status logic
    if end < TODAY - timedelta(days=30):
        status = "Closed"
    elif start > TODAY:
        status = "Planned"
    else:
        status = "In Progress"

    audit_rows.append({
        "audit_id": audit_id,
        "audit_type": audit_type,
        "scope": f"{audit_type} - {dept['department_name']} at {station['station_code']}",
        "start_date": start.date(),
        "end_date": end.date(),
        "station_code": station["station_code"],
        "department_id": int(dept["department_id"]),
        "is_provider_audit": is_provider,
        "provider_type": provider_type,
        "lead_auditor": f"Auditor {np.random.randint(1, 11):02d}",
        "status": status
    })

audits = pd.DataFrame(audit_rows)

# -------------------------------------------------------------------
# 6. Findings fact table
# -------------------------------------------------------------------
severity_levels = ["Low", "Medium", "High", "Critical"]
severity_probs = [0.4, 0.35, 0.2, 0.05]
# Scores for risk_index calculation (probability_score 1–5)
severity_scores = {"Low": 1, "Medium": 2, "High": 4, "Critical": 5}

categories = ["Documentation", "Training", "Operations", "Facilities", "Equipment", "Human Factors"]

findings_rows = []
finding_id = 1

for _, audit in audits.iterrows():
    # Number of findings per audit (5–24)
    n_findings = int(np.random.randint(5, 25))

    dept_row = departments.loc[departments["department_id"] == audit["department_id"]].iloc[0]
    dept_code = dept_row["department_code"]
    possible_disciplines = dept_to_disciplines.get(dept_code, ["ORG"])

    for _ in range(n_findings):
        severity = np.random.choice(severity_levels, p=severity_probs)
        category = np.random.choice(categories)
        discipline_code = np.random.choice(possible_disciplines)

        # date_raised between start_date and (end_date + 10 days)
        start = datetime.combine(audit["start_date"], datetime.min.time())
        end = datetime.combine(audit["end_date"], datetime.min.time()) + timedelta(days=10)
        span_days = max(1, (end - start).days)
        date_raised = start + timedelta(days=int(np.random.randint(0, span_days)))

        # due_date 30–90 days after date_raised
        due_date = date_raised + timedelta(days=int(np.random.randint(30, 91)))

        # Decide if finding is closed (80% chance)
        is_closed = np.random.rand() < 0.8
        date_closed = None
        status = None
        closed_on_time = None

        if is_closed:
            # Different closure speeds before/after CAPA_GO_LIVE
            if date_raised < CAPA_GO_LIVE:
                closure_days = int(np.random.normal(loc=70, scale=20))
            else:
                closure_days = int(np.random.normal(loc=45, scale=15))

            closure_days = max(5, closure_days)  # at least 5 days
            date_closed = date_raised + timedelta(days=closure_days)

            # Cap at TODAY (can't close in the future)
            if date_closed > TODAY:
                date_closed = TODAY

            closed_on_time = date_closed <= due_date
            status = "Closed"
        else:
            # Still open
            date_closed = None
            if due_date.date() < TODAY.date():
                status = "Overdue"
            else:
                status = "Open"
            closed_on_time = False

        # Probability score (1–5), slightly biased higher for high/critical
        probability_score = int(np.random.randint(1, 6))
        if severity in ["High", "Critical"] and probability_score < 3:
            probability_score += 2  # bump it up a bit

        risk_index = severity_scores[severity] * probability_score

        repeat_flag = bool(np.random.rand() < 0.15)  # ~15% repeats

        findings_rows.append({
            "finding_id": finding_id,
            "audit_id": int(audit["audit_id"]),
            "severity": severity,
            "category": category,
            "iosa_discipline_code": discipline_code,
            "standard_ref": f"{discipline_code}-{np.random.randint(100, 999)}",
            "description": f"Synthetic finding {finding_id} in {category.lower()} category.",
            "risk_index": int(risk_index),
            "date_raised": date_raised.date(),
            "date_closed": date_closed.date() if date_closed else None,
            "due_date": due_date.date(),
            "status": status,  # Open / Overdue / Closed
            "repeat_flag": repeat_flag,
            "root_cause": np.random.choice(
                ["Procedure not followed", "Training gap", "Documentation gap",
                 "Resource limitation", "Process design"],
                p=[0.3, 0.2, 0.2, 0.15, 0.15]
            ),
            "responsible_owner": f"Owner {np.random.randint(1, 21):02d}",
            "probability_score": probability_score,
            "closed_on_time": closed_on_time
        })

        finding_id += 1

findings = pd.DataFrame(findings_rows)

# -------------------------------------------------------------------
# 7. Save to CSV
# -------------------------------------------------------------------
iosa_disciplines.to_csv("data/iosa_disciplines.csv", index=False)
departments.to_csv("data/departments.csv", index=False)
stations.to_csv("data/stations.csv", index=False)
calendar.to_csv("data/calendar.csv", index=False)
audits.to_csv("data/audits.csv", index=False)
findings.to_csv("data/findings.csv", index=False)

print("Done! Generated:")
print(f"- {len(iosa_disciplines)} IOSA disciplines")
print(f"- {len(departments)} departments")
print(f"- {len(stations)} stations")
print(f"- {len(calendar)} calendar dates")
print(f"- {len(audits)} audits")
print(f"- {len(findings)} findings")
