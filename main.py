# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Hello, World!"


# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
import pandas as pd
from geopy.distance import geodesic

from scraper import scrape


def calculate_distance(job_location, user_location):
    job_coords = (job_location[0], job_location[1])
    return geodesic(job_coords, user_location).km


parsed_jobs = scrape()
job_df = pd.DataFrame(parsed_jobs)

user_info = {
    "experience": "Junior",
    "preferedCompanySize": "medium",
    "location": [37.7749, -122.4194],
    "skills": ["Python", "Java", "C++"],
}


print(job_df["skills"].str.get_dummies(sep=","))
