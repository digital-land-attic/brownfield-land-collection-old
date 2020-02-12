#!/usr/bin/env python3

import os
from pyquery import PyQuery
from urllib.parse import urljoin
import requests


save_dir = "var/data-gov-uk"


def save(path, data):
    print(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


url = "https://data.gov.uk/search?q=brownfield"

while url:
    print("#", url)
    d = PyQuery(url=url)

    for link in d.items(".dgu-results__result a"):
        href = link.attr["href"]
        key = href.split("/")[2]
        response = requests.get(
            "https://ckan.publishing.service.gov.uk/api/3/action/package_show?id=%s"
            % (key)
        )
        save("save_dir/%s" % (save_dir, key), response.content)
        print(key)

    next_url = d("a[rel='next']").attr["href"]
    url = urljoin(url, next_url) if next_url else None
