#!/usr/bin/env python3

#
#  hack to add a file to the collection manually
#
from sys import argv
import os
from datetime import datetime
import logging
import hashlib
import canonicaljson

headers_dir = "collection/headers/"
bodies_dir = "collection/bodies/"


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def addone(dataset, organisation, path):
    headers = {
        "dataset": dataset,
        "organisation": organisation,
        "datetime": datetime.utcnow().isoformat(),
    }

    headers_key = hashlib.sha256(path.encode("utf-8")).hexdigest()
    headers_path = os.path.join(
        headers_dir, headers["datetime"][:10], headers_key + ".json"
    )

    with open(path, mode="rb") as f:
        content = f.read()

    body_key = hashlib.sha256(content).hexdigest()
    headers["body"] = body_key
    save(os.path.join(bodies_dir, body_key), content)

    headers_json = canonicaljson.encode_canonical_json(headers)
    save(headers_path, headers_json)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    addone(argv[1], argv[2], argv[3])
