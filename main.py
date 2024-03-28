# from flask import Flask

# app = Flask(__name__)


# @app.route("/")
# def home():
#     return "Hello, World!"


# if __name__ == "__main__":
#     app.run(port=8000, debug=True)
import pandas as pd
from geopy.distance import geodesic
from sklearn.compose import make_column_transformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline

from scraper import scrape


def calculate_distance(job_location, user_location):
    job_coords = (job_location[0], job_location[1])
    return geodesic(job_coords, user_location).km


parsed_jobs = scrape()
job_df = pd.DataFrame(parsed_jobs)


col_transformer = make_column_transformer(
    (CountVectorizer(), "skills"),
    remainder="drop",
)
pipeline = make_pipeline(col_transformer, KNeighborsClassifier(n_neighbors=10))

X_train = job_df[["skills"]]
y_train = job_df["title"]
X_test = pd.DataFrame({"skills": "Java"}, index=[0])

pipeline.fit(X_train, y_train)
job_title = pipeline.predict(X_test)

# get row that has that title
print(job_df[job_df["title"] == job_title[0]])
