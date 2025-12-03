import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "audit.db"

query = """
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
"""

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute(query)
rows = cur.fetchall()
conn.close()

for row in rows:
    print(row)
