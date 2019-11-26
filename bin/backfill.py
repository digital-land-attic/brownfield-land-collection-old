#!/usr/bin/env python3

#
#  hack to add a file to the collection manually
#
from sys import argv, exit
import os
from datetime import datetime
import logging
import hashlib
import canonicaljson
import csv

headers_dir = "collection/log/"
resource_dir = "collection/resource/"


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def addone(path, url):
    headers = {
        # "datetime": datetime.utcnow().isoformat(),
        "datetime": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
        "url": url,
    }

    headers_key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    headers_path = os.path.join(
        headers_dir, headers["datetime"][:10], headers_key + ".json"
    )

    with open(path, mode="rb") as f:
        content = f.read()

    resource = hashlib.sha256(content).hexdigest()
    headers["resource"] = resource
    save(os.path.join(resource_dir, resource), content)

    headers_json = canonicaljson.encode_canonical_json(headers)
    save(headers_path, headers_json)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    # brownfield-site-publication^Iorganisation^Idocumentation-url^Idata-url^Idata-gov-uk^Istart-date^Iend-date$

    for row in csv.DictReader(
        open(
            "/home/psd/src/communitiesuk/digital-land-collector/etc/brownfield-site-publication.tsv"
        ),
        delimiter="\t",
    ):
        path = row["organisation"]
        path = path.replace("local-authority-eng:", "")
        path = path.replace("development-corporation:", "dc")
        path = path.replace("national-park:", "np")
        path = (
            "/home/psd/src/communitiesuk/digital-land-collector/var/cache/brownfield-sites-"
            + path
            + row["suffix"]
        )
        url = row["data-url"]
        if os.path.isfile(path):
            addone(path, url)
