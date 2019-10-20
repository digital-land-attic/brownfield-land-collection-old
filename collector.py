#!/usr/bin/env python3

#
#  simple data collector
#
import os
from datetime import datetime
from timeit import default_timer as timer
import logging
import requests
import hashlib
import canonicaljson
import csv

user_agent = "Digital Land data collector"
headers_dir = "collection/headers/"
bodies_dir = "collection/bodies/"
datasets_dir = "datasets/"


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def fetch(dataset, organisation, url):
    if not url:
        return

    headers = {
        "dataset": dataset,
        "organisation": organisation,
        "url": url,
        "datetime": datetime.utcnow().isoformat(),
    }

    headers_key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    headers_path = os.path.join(
        headers_dir, headers["datetime"][:10], headers_key + ".json"
    )

    if os.path.isfile(headers_path):
        return

    logging.info(" ".join([dataset, organisation, url]))

    try:
        start = timer()
        response = requests.get(url, headers={"User-Agent": user_agent})
    except (
        requests.ConnectionError,
        requests.Timeout,
        requests.TooManyRedirects,
        requests.exceptions.MissingSchema,
    ) as exception:
        logging.warning(exception)
        headers["exception"] = type(exception).__name__
        response = None
    finally:
        headers["elapsed"] = str(round(timer() - start, 3))

    if response:
        headers["request-headers"] = dict(response.request.headers)
        headers["response-headers"] = dict(response.headers)
        headers["status"] = str(response.status_code)

        if headers["status"] == "200":
            body_key = hashlib.sha256(response.content).hexdigest()
            headers["body"] = body_key
            save(os.path.join(bodies_dir, body_key), response.content)

    headers_json = canonicaljson.encode_canonical_json(headers)
    save(headers_path, headers_json)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    for row in csv.DictReader(open(os.path.join(datasets_dir, "dataset" + ".csv"))):
        dataset = row["dataset"]
        for row in csv.DictReader(open(os.path.join(datasets_dir, dataset + ".csv"))):
            fetch(dataset, row["organisation"], row["resource-url"])
