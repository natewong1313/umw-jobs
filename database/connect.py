import os

import psycopg2


def connect():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


# create the jobs table on startup
def setup_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id VARCHAR(50) PRIMARY KEY,
            type TEXT,
            position TEXT,
            company_name TEXT,
            company_logo TEXT,
            link TEXT,
            description TEXT,
            qualifications TEXT,
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            city TEXT,
            state TEXT,
            is_remote BOOLEAN,
            posted_on NUMERIC(10, 0)
        )
        """
    )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(50) PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            completed_onboarding BOOLEAN DEFAULT FALSE,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            experience_level VARCHAR(100),
            skills TEXT,
            job_type VARCHAR(100)
        )
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_jobs (
            user_id VARCHAR(50) NOT NULL,
            job_id VARCHAR(50) NOT NULL,
            PRIMARY KEY (user_id, job_id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id)
                   )
        """)
    conn.commit()
    cursor.close()
    conn.close()
