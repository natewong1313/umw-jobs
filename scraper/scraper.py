import os

import requests


def scrape_jobs(search_term):
    querystring = {"query": search_term, "page": "2", "num_pages": "10"}
    headers = {
        "X-RapidAPI-Key": os.getenv("API_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }
    response = requests.get(
        "https://jsearch.p.rapidapi.com/search", headers=headers, params=querystring
    )
    return response.json()["data"]
