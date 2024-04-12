import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

from scraper import scrape

parsed_jobs = scrape()
job_df = pd.DataFrame(parsed_jobs)


def find_jobs(user):
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
