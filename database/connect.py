import os

import psycopg2


# create the jobs table on startup
def setup_db():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id VARCHAR(50) PRIMARY KEY,
            position VARCHAR(100) NOT NULL,
            company_name VARCHAR(100) NOT NULL,
            link VARCHAR(255),
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            description TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(50) PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            completed_onboarding BOOLEAN DEFAULT FALSE,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            latitude DECIMAL(10, 6),
            longitude DECIMAL(10, 6),
            experience_level VARCHAR(100),
            skills TEXT
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def connect():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
