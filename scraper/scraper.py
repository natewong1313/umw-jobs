import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "text/plain",
    "Origin": "https://simplify.jobs",
    "Connection": "keep-alive",
    "Referer": "https://simplify.jobs/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}

params = {
    "x-typesense-api-key": "sUjQlkfBFnglUFcsFsZVcE7xhI8lJ1RG",
}

data = {
    "searches": [
        {
            "query_by": "title,company_name,locations",
            "per_page": 200,
            "sort_by": "_text_match:desc,posting_id:desc",
            "highlight_full_fields": "title,company_name,locations",
            "collection": "jobs",
            "q": "*",
            "facet_by": "countries,degrees,experience_level,functions,locations",
            "filter_by": "experience_level:=[`Junior`] && functions:=[`Software Engineering`]",
            "max_facet_values": 50,
            "page": 2,
        },
    ]
}


# scrapes job listings
def scrape():
    response = requests.post(
        "https://xv95tgzrem61cja4p.a1.typesense.net/multi_search",
        params=params,
        headers=headers,
        json=data,
    )
    response_json = response.json()

    # db_connection = connect()
    parsed_jobs = []
    for result in response_json["results"]:
        for hit in result["hits"]:
            jobs = parse_job(hit["document"])
            for job in jobs:
                parsed_jobs.append(job)
    print(len(parsed_jobs))
    return parsed_jobs


def parse_job(job_data):
    base_job = {
        "id": job_data["posting_id"],
        "title": job_data["title"],
        "type": job_data["type"],
        "url": job_data["url"],
        "company": {"name": job_data["company_name"], "logo": job_data["company_logo"]},
        "experience_levels": ",".join(job_data["experience_level"]),
        # "locations": job_data["geolocations"],
        "remote": job_data["remote"],
        "skills": ",".join(job_data["skills"]),
    }
    if len(job_data["geolocations"]) == 0:
        base_job["location"] = None
        return [base_job]
    else:
        jobs = []
        for coords in job_data["geolocations"]:
            job = base_job.copy()
            job["location"] = (coords[0], coords[1])
            jobs.append(job)
        return jobs
