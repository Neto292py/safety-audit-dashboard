"""
Load synthetic safety & audit CSVs into a SQLite database.

Creates a file called 'audit.db' in the project folder with these tables:
- iosa_disciplines
- departments
- stations
- calendar
- audits
- findings
"""

import sqlite3
from pathlib import Path

import pandas as pd

# -------------------------------------------------------------------
# 1. Paths and connection
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "audit.db"

print(f"Base directory: {BASE_DIR}")
print(f"Data directory: {DATA_DIR}")
print(f"Database path: {DB_PATH}")

# Connect to SQLite (this will create the file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)

# Optional: enable foreign keys (won't hurt even if we don't define FKs yet)
conn.execute("PRAGMA foreign_keys = ON;")

# -------------------------------------------------------------------
# 2. Helper to load a CSV into a table
# -------------------------------------------------------------------
def load_csv_to_table(csv_name: str, table_name: str):
    csv_path = DATA_DIR / csv_name
    print(f"Loading {csv_path} into table '{table_name}'...")
    df = pd.read_csv(csv_path)
    # if_exists='replace' means: drop table if exists, then create from df
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"  -> {len(df)} rows inserted into {table_name}.")

# -------------------------------------------------------------------
# 3. Load all dimension and fact tables
# -------------------------------------------------------------------
load_csv_to_table("iosa_disciplines.csv", "iosa_disciplines")
load_csv_to_table("departments.csv", "departments")
load_csv_to_table("stations.csv", "stations")
load_csv_to_table("calendar.csv", "calendar")
load_csv_to_table("audits.csv", "audits")
load_csv_to_table("findings.csv", "findings")

# -------------------------------------------------------------------
# 4. Quick sanity check with a SQL query
# -------------------------------------------------------------------
print("\nRunning a quick sanity check query on findings...")
query = """
SELECT
    COUNT(*) AS total_findings,
    SUM(CASE WHEN severity IN ('High', 'Critical') THEN 1 ELSE 0 END) AS high_critical_findings
FROM findings;
"""
check_df = pd.read_sql_query(query, conn)
print(check_df)

conn.close()
print("\nDone. SQLite database created at:", DB_PATH)
