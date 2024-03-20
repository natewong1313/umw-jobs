import sqlite3


# create the jobs table on startup
def setup_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT,
    type TEXT,
    url TEXT,
    company_name TEXT,
    company_logo TEXT,
    experience_levels TEXT,
    latitude REAL,
    longitude REAL,
    remote INTEGER,
    skills TEXT
)
""")
    conn.commit()
    conn.close()


def connect():
    return sqlite3.connect("database.db")
