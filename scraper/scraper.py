import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Content-Type": "text/plain",
    "Origin": "https://simplify.jobs",
    "Connection": "keep-alive",
    "Referer": "https://simplify.jobs/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

params = {
    "x-typesense-api-key": "sUjQlkfBFnglUFcsFsZVcE7xhI8lJ1RG",
}

data = '{"searches":[{"query_by":"title,company_name,locations","per_page":21,"sort_by":"_text_match:desc,posting_id:desc","highlight_full_fields":"title,company_name,locations","collection":"jobs","q":"*","facet_by":"countries,degrees,experience_level,functions,locations","filter_by":"experience_level:=[`Junior`] && functions:=[`Software Engineering`]","max_facet_values":50,"page":1},{"query_by":"title,company_name,locations","per_page":21,"sort_by":"_text_match:desc,posting_id:desc","highlight_full_fields":"title,company_name,locations","collection":"jobs","q":"*","facet_by":"experience_level","filter_by":"functions:=[`Software Engineering`]","max_facet_values":50,"page":1},{"query_by":"title,company_name,locations","per_page":21,"sort_by":"_text_match:desc,posting_id:desc","highlight_full_fields":"title,company_name,locations","collection":"jobs","q":"*","facet_by":"functions","filter_by":"experience_level:=[`Junior`]","max_facet_values":50,"page":1}]}'

response = requests.post(
    "https://xv95tgzrem61cja4p.a1.typesense.net/multi_search",
    params=params,
    headers=headers,
    data=data,
)

print(response.text)
