import requests

from database import connect

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
print(connect)
params = {
    "x-typesense-api-key": "sUjQlkfBFnglUFcsFsZVcE7xhI8lJ1RG",
}

data = {
    "searches": [
        {
            "query_by": "title,company_name,locations",
            "per_page": 100,
            "sort_by": "_text_match:desc,posting_id:desc",
            "highlight_full_fields": "title,company_name,locations",
            "collection": "jobs",
            "q": "*",
            "facet_by": "countries,degrees,experience_level,functions,locations",
            "filter_by": "experience_level:=[`Junior`] && functions:=[`Software Engineering`]",
            "max_facet_values": 50,
            "page": 1,
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
            parsed_job = parse_job(hit["document"])
            # print(parsed_job)
            parsed_jobs.append(parsed_job)
            # job_data = hit["document"]
            # db_connection.execute(
            #     """
            # INSERT OR IGNORE INTO jobs (id, title, type, url, company_name, company_logo, experience_levels, latitude, longitude, remote, skills)
            # VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            # """,
            #     (
            #         job_data["posting_id"],
            #         job_data["title"],
            #         job_data["type"],
            #         job_data["url"],
            #         job_data["company_name"],
            #         job_data["company_logo"],
            #         ",".join(job_data["experience_level"]),
            #         job_data["geolocations"][0],
            #         job_data["geolocations"][1],
            #         int(job_data["remote"]),
            #         ",".join(job_data["skills"]),
            #     ),
            # )
    # db_connection.commit()
    # db_connection.close()
    # print(parsed_jobs)
    # with open("out.json", "w") as out_file:
    #     json.dump(response_json, out_file, indent=2, sort_keys=True)
    return parsed_jobs


def parse_job(job_data):
    return {
        "id": job_data["posting_id"],
        "title": job_data["title"],
        "type": job_data["type"],
        "url": job_data["url"],
        "company": {"name": job_data["company_name"], "logo": job_data["company_logo"]},
        "experience_levels": ",".join(job_data["experience_level"]),
        "locations": job_data["geolocations"],
        "remote": job_data["remote"],
        "skills": ",".join(job_data["skills"]),
    }
