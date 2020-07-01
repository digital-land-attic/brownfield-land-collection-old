#!/usr/bin/env python
import logging
import sys
import hashlib
import csv

logging.basicConfig(level=logging.INFO)


def url_endpoint(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


fieldnames = [
    "endpoint",
    "endpoint-url",
    "organisation",
    "method",
    "start-date",
    "end-date",
]
writer = csv.DictWriter(open("collection/endpoint.csv", "w"), fieldnames=fieldnames)
writer.writeheader()

count = 0

for row in csv.DictReader(open("dataset/brownfield-land.csv")):
    logging.debug(row)
    url = row["resource-url"]
    writer.writerow(
        {
            "endpoint": url_endpoint(url),
            "endpoint-url": url,
            "organisation": row["organisation"],
            "method": None,
            "start-date": row["start-date"],
            "end-date": row["end-date"],
        }
    )
    count += 1

logging.info("Complete - %d rows written" % count)
