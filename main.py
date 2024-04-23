import os

import workos
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, UserMixin, current_user, login_user
from uszipcode import SearchEngine

from database import connect, setup_db
from model import find_jobs, get_skills

load_dotenv()
setup_db()

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/static")
app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
app.config["SECRET_KEY"] = "3ecc98112e60c356c9ab250c"
app.config["TEMPLATES_AUTO_RELOAD"] = True

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(
        self,
        id,
        email,
        completed_onboarding,
        first_name,
        last_name,
        latitude,
        longitude,
        experience_level,
        skills,
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


@login_manager.user_loader
def user_loader(id: str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None:
        return None
    return User(
        user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8]
    )


def add_user(user):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (id, email) VALUES (%s, %s)",
        (user.id, user.email),
    )
    conn.commit()
    cursor.close()
    conn.close()


workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")


def coords_to_location(latitude, longitude):
    search = SearchEngine()
    print(float(latitude), float(longitude))
    return search.by_coordinates(float(latitude), float(longitude), returns=1)[
        0
    ].major_city


app.jinja_env.globals.update(coords_to_location=coords_to_location)


@app.route("/")
def home():
    if current_user.is_authenticated and current_user.completed_onboarding:
        jobs = find_jobs(
            {
                "skills": current_user.skills,
                "experience_level": current_user.experience_level,
            }
        )
        return render_template("home.html", user=current_user, jobs=jobs)
    elif current_user.is_authenticated:
        return render_template("home.html", user=current_user, skills=get_skills())
    return render_template("signin.html")


@app.route("/email-sent")
def email_sent():
    return render_template("email_sent.html")


@app.route("/auth", methods=["POST"])
def auth():
    email = request.form["email"]

    session = workos.client.passwordless.create_session(
        {"email": email, "type": "MagicLink"}
    )

    workos.client.passwordless.send_session(session["id"])
    return redirect("/email-sent")


@app.route("/callback")
def callback():
    code = request.args.get("code")
    profile_and_token = workos.client.sso.get_profile_and_token(code)

    profile = profile_and_token.profile.to_dict()

    user = User(profile["id"], profile["email"])
    add_user(user)
    login_user(user)
    return redirect("/")


@app.route("/complete-onboarding", methods=["POST"])
def complete_onboarding():
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    zip_code = request.form["zipCode"]
    experience_level = request.form["experienceLevel"]
    skills = ",".join(request.form.getlist("skills"))

    search = SearchEngine()
    location_data = search.by_zipcode(zip_code)
    latitude = location_data.lat
    longitude = location_data.lng

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET completed_onboarding = %s, first_name = %s, last_name = %s, latitude = %s, longitude = %s, experience_level = %s, skills = %s WHERE id = %s",
        (
            True,
            first_name,
            last_name,
            latitude,
            longitude,
            experience_level,
            skills,
            current_user.id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
# import pandas as pd
# from geopy.distance import geodesic
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import pairwise_distances

# from scraper import scrape


# def calculate_distance(job_location, user_location):
#     print(job_location)
#     if job_location is None:
#         return 0
#     return geodesic(job_location, user_location).km


# parsed_jobs = scrape()
# job_df = pd.DataFrame(parsed_jobs)

# user = {
#     "skills": "Python,Java,Go,React.js",
#     "experience_level": "Junior",
#     "location": (37.7749, -122.4194),
# }


# def find_jobs_for_user(user):
#     filtered_job_df = job_df[
#         job_df["experience_levels"].str.contains(user["experience_level"])
#     ]

#     vec = TfidfVectorizer()
#     vec.fit(filtered_job_df["skills"])
#     tfidf_matrix = vec.transform(filtered_job_df["skills"])

#     user_features = user["skills"].lower()
#     user_vec = vec.transform([user_features])

#     similarities = pairwise_distances(user_vec, tfidf_matrix, metric="cosine")

#     matches = similarities.argsort()[0][:5]

#     for i, row in enumerate(matches):
#         job = filtered_job_df.iloc[row]
#         print(job["title"] + " | " + job["skills"])


# find_jobs_for_user(user)
