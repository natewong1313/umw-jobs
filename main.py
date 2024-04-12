import os

import workos
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request

load_dotenv()
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/static")
app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
app.config["SECRET_KEY"] = "3ecc98112e60c356c9ab250c"
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# app.config["GITHUB_CLIENT_ID"] = "d12a2f046de2cbf7efcb"
# app.config["GITHUB_CLIENT_SECRET"] = "219c4fd176526b51fc213ebf91ccd29585a70c4d"
# app.config["GITHUB_ACCESS_TOKEN_URL"] = "https://github.com/login/oauth/access_token"
# app.config["GITHUB_ACCESS_TOKEN_PARAMS"] = None
# app.config["GITHUB_AUTHORIZE_URL"] = "https://github.com/login/oauth/authorize"
# app.config["GITHUB_AUTHORIZE_PARAMS"] = None
# app.config["GITHUB_API_BASE_URL"] = "https://api.github.com"
# app.config["GITHUB_CLIENT_KWARGS"] = {"scope": "user:email"}

# oauth = OAuth(app)
# oauth.register(
#     name="github",
#     client_id=app.config["GITHUB_CLIENT_ID"],
#     client_secret=app.config["GITHUB_CLIENT_SECRET"],
#     authorize_url=app.config["GITHUB_AUTHORIZE_URL"],
#     access_token_url=app.config["GITHUB_ACCESS_TOKEN_URL"],
#     client_kwargs=app.config["GITHUB_CLIENT_KWARGS"],
# )

workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")


@app.route("/")
def home():
    return render_template("signin.html")


@app.route("/email-sent")
def email_sent():
    return render_template("email_sent.html")


# @app.route("/login")
# def login():
#     redirect_uri = url_for("callback", _external=True)
#     return oauth.github.authorize_redirect(redirect_uri)


# @app.route("/callback")
# def callback():
#     token = oauth.github.authorize_access_token()
#     user = token.get("userinfo")
#     if not user:
#         print(oauth.github.userinfo())
#     return redirect("/")
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

    profile = profile_and_token.profile
    # {
    #     "id": "prof_01HV99BT1PKX9G6VXYAME0629X",
    #     "email": "natewong1@gmail.com",
    #     "first_name": None,
    #     "last_name": None,
    #     "groups": None,
    #     "organization_id": None,
    #     "connection_id": "conn_01HV998FA8VM5ZYMYPVZT6VKVZ",
    #     "connection_type": "MagicLink",
    #     "idp_id": "natewong1@gmail.com",
    #     "raw_attributes": {},
    # }
    print(profile.to_dict())

    # Use the information in `profile` for further business logic.

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
