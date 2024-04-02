# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Hello, World!"


# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
import pandas as pd
from geopy.distance import geodesic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from scraper import scrape


def calculate_distance(job_location, user_location):
    job_coords = (job_location[0], job_location[1])
    return geodesic(job_coords, user_location).km


parsed_jobs = scrape()
job_df = pd.DataFrame(parsed_jobs)

user = {"skills": "Python,Java", "experience_level": "Junior"}


def find_jobs_for_user(user):
    filtered_job_df = job_df[
        job_df["experience_levels"].str.contains(user["experience_level"])
    ]

    vec = TfidfVectorizer()
    vec.fit(filtered_job_df["skills"])
    tfidf_matrix = vec.transform(filtered_job_df["skills"])

    user_features = user["skills"].lower()
    user_vec = vec.transform([user_features])

    similarities = pairwise_distances(user_vec, tfidf_matrix, metric="cosine")

    matches = similarities.argsort()[0][:5]

    for i, row in enumerate(matches):
        job = filtered_job_df.iloc[row]
        print(job["title"] + " | " + job["skills"])


find_jobs_for_user(user)
