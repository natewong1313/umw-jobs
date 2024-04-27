import json
import os

import workos
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, current_user, login_user
from uszipcode import SearchEngine

from database import (
    connect,
    format_jobs_from_db,
    get_jobs,
    get_matches,
    setup_db,
)
from database.user import User, check_user_exists, load_user
from model import process_jobs

# from model import get_skills

load_dotenv()
setup_db()

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/static")
app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
app.config["SECRET_KEY"] = "3ecc98112e60c356c9ab250c"
app.config["TEMPLATES_AUTO_RELOAD"] = True

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id: str):
    conn = connect()
    return load_user(id, conn)


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
    result = search.by_coordinates(float(latitude), float(longitude), returns=1)[0]
    return result.post_office_city


app.jinja_env.globals.update(coords_to_location=coords_to_location)

f = open("./out.json", encoding="utf8")

data = json.load(f)["data"]


@app.route("/")
def home():
    if current_user.is_authenticated and current_user.completed_onboarding:
        print(request.args.get("remoteOnly"))
        print(request.args.get("distance"))
        jobs = format_jobs_from_db(
            get_jobs("software engineer intern"),
            current_user.latitude,
            current_user.longitude,
        )
        best_jobs = process_jobs(
            jobs,
            current_user,
            request.args.get("remoteOnly"),
            request.args.get("distance"),
        )
        return render_template("home.html", user=current_user, jobs=best_jobs)
    elif current_user.is_authenticated:
        return render_template(
            "home.html",
            user=current_user,
            skills=[
                "Python",
                "Java",
                "JavaScript",
                "C++",
                "C#",
                "Ruby",
                "Swift",
                "Kotlin",
                "PHP",
                "Go",
                "Rust",
                "SwiftUI",
                "React",
                "Angular",
                "Vue.js",
                "HTML",
                "CSS",
                "SQL",
                "MySQL",
                "PostgreSQL",
                "MongoDB",
                "Redis",
                "Docker",
                "Kubernetes",
                "AWS",
                "Azure",
                "Google Cloud",
                "Git",
                "GitHub",
                "JIRA",
                "Agile",
                "Scrum",
                "Test-Driven Development",
                "Behavior-Driven Development",
                "Microservices",
                "API Design",
                "Cloud Computing",
                "DevOps",
                "Continuous Integration",
                "Continuous Deployment",
                "Continuous Monitoring",
                "Machine Learning",
                "Artificial Intelligence",
                "Natural Language Processing",
                "Data Science",
                "Data Analysis",
                "Data Visualization",
                "Web Development",
                "Mobile App Development",
                "Game Development",
                "Network Programming",
                "Operating Systems",
                "Database Administration",
                "Cybersecurity",
                "Ethical Hacking",
                "Penetration Testing",
                "Vulnerability Assessment",
                "Compliance",
                "Auditing",
                "Incident Response",
            ],
        )
    return render_template("signin.html")


@app.route("/email-sent")
def email_sent():
    return render_template("email_sent.html")


@app.route("/matches")
def matches():
    if current_user.is_authenticated and current_user.completed_onboarding:
        matches = format_jobs_from_db(
            get_matches(current_user.id), current_user.latitude, current_user.longitude
        )
        return render_template("matches.html", user=current_user, jobs=matches)
    return redirect("/")


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

    if check_user_exists(profile["id"], connect()):
        user = load_user(profile["id"], connect())
    else:
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
    preffered_job_type = request.form["jobType"]

    search = SearchEngine()
    location_data = search.by_zipcode(zip_code)
    latitude = location_data.lat
    longitude = location_data.lng

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET completed_onboarding = %s, first_name = %s, last_name = %s, latitude = %s, longitude = %s, experience_level = %s, skills = %s, job_type=%s WHERE id = %s",
        (
            True,
            first_name,
            last_name,
            latitude,
            longitude,
            experience_level,
            skills,
            preffered_job_type,
            current_user.id,
        ),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/add-match", methods=["POST"])
def add_match():
    jobId = request.get_json()["jobId"]
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """ INSERT INTO user_jobs (user_id, job_id) VALUES (%s, %s)""",
        (current_user.id, jobId),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return "ok"


if __name__ == "__main__":
    app.run(port=8000, debug=os.getenv("DEBUG") == "True")
