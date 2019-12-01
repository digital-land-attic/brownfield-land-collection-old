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

headers_dir = "collection/log/"
resource_dir = "collection/resource/"


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def addone(path, url):
    headers = {
        "datetime": datetime.utcnow().isoformat(),
        # "datetime": datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
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
    addone(argv[1], argv[2])
