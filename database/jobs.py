from datetime import datetime

from geopy import distance

from .connect import connect


# Add newly scraped jobs to the database
def add_new_jobs(jobs, job_type):
    conn = connect()
    cursor = conn.cursor()

    for job in jobs:
        qualifications = ""
        if "Qualifications" in job["job_highlights"]:
            qualifications = " ".join(job["job_highlights"]["Qualifications"])
        cursor.execute(
            """
            INSERT INTO jobs (
                id,
                type,
                position,
                company_name,
                company_logo,
                link,
                description,
                qualifications,
                latitude,
                longitude,
                city,
                state,
                is_remote,
                posted_on
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING""",
            (
                job["job_id"],
                job_type,
                job["job_title"],
                job["employer_name"],
                job["employer_logo"],
                job["job_apply_link"],
                job["job_description"],
                qualifications,
                job["job_latitude"],
                job["job_longitude"],
                job["job_city"],
                job["job_state"],
                job["job_is_remote"],
                job["job_posted_at_timestamp"],
            ),
        )
    conn.commit()
    cursor.close()
    conn.close()


# get jobs based on type, e.g. "Software engineer intern"
def get_jobs(job_type):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE type = %s", (job_type,))
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jobs


# format jobs from the database, which are in a list, to a dict format
def format_jobs_from_db(jobs, user_lat, user_lon):
    formatted_jobs = []
    for job in jobs:
        formatted_jobs.append(
            {
                "id": job[0],
                "type": job[1],
                "title": job[2],
                "employer": job[3],
                "employer_logo": job[4],
                "link": job[5],
                "description": job[6],
                "qualifications": job[7],
                "latitude": job[8],
                "longitude": job[9],
                "city": job[10],
                "state": job[11],
                "is_remote": job[12],
                "posted_at": job[13],
                "posted_at_readable": datetime.fromtimestamp(int(job[13])),
                "distance": distance.distance(
                    (user_lat, user_lon), (job[8], job[9])
                ).miles,
            }
        )
    return formatted_jobs


# get all of the users matches
def get_matches(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_jobs WHERE user_id = %s", (user_id,))
    matches = cursor.fetchall()

    jobs = []
    for match in matches:
        cursor.execute("SELECT * FROM jobs WHERE id = %s", (match[1],))
        job = cursor.fetchone()
        jobs.append(job)

    cursor.close()
    conn.close()
    return jobs
