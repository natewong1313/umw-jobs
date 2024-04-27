import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def pre_processor(text):
    text = text.lower().replace("c#", "csharp")
    text = text.replace("c++", "cplusplus")
    text = text.replace("c+", "cplusplus")
    text = text.replace("react native", "reactnative")
    text = text.replace(".net", "dotnet")
    text = text.replace("node.js", "node")
    return text


def process_jobs(jobs, user, remote_only, max_distance):
    job_df = pd.DataFrame(jobs)
    job_df.set_index("id", inplace=True)
    job_df["job_full_description"] = (
        job_df["description"] + " " + job_df["qualifications"]
    )

    if remote_only == "Yes":
        job_df = job_df[job_df["is_remote"]]
    if max_distance != "" and max_distance is not None:
        max_distance = int(max_distance)
        job_df = job_df[job_df["distance"] <= max_distance]

    vec = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    vec.fit(job_df["job_full_description"])

    user_tfidf = vec.transform([user.skills])
    jobs_tfidf = vec.transform(job_df["job_full_description"])

    model = NearestNeighbors(n_neighbors=10, metric="cosine")
    model.fit(jobs_tfidf)

    distances, indices = model.kneighbors(user_tfidf)
    nearest_jobs = job_df.iloc[indices[0]]

    return [job for job in jobs if job["id"] in nearest_jobs.index]
