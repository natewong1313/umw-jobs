from flask_login import UserMixin


class User(UserMixin):
    def __init__(
        self,
        id,
        email,
        completed_onboarding=None,
        first_name=None,
        last_name=None,
        latitude=None,
        longitude=None,
        experience_level=None,
        skills=None,
        job_type=None,
    ):
        self.id = id
        self.email = email
        self.completed_onboarding = completed_onboarding
        self.first_name = first_name
        self.last_name = last_name
        self.latitude = latitude
        self.longitude = longitude
        self.experience_level = experience_level
        self.skills = skills
        self.job_type = job_type


def load_user(id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return None
    return User(
        user[0],
        user[1],
        user[2],
        user[3],
        user[4],
        user[5],
        user[6],
        user[7],
        user[8],
    )


def check_user_exists(id, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user is not None
