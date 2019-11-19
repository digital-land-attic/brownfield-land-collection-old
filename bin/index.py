#!/usr/bin/env python3

#
#  create an index for a collection
#
import os
import re
import glob
from datetime import datetime
import logging
import json
import canonicaljson

idx = {}


def parse_path(path):
    m = re.match(r"^.*\/([-\d]+)\/(\w+).json", path)
    return m.groups()


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def add(date, key, h):

    e = {}
    for field in ["status", "exception", "datetime", "elapsed", "resource"]:
        if field in h and h[field]:
            e[field] = h[field]

    if h.get('status', '') == '200' and 'response-headers' in h:
        for field in ["Content-Type", "Content-Length"]:
            if field in h['response-headers']:
                e[field] = h['response-headers'][field]

    idx.setdefault(key, {"url": h.get("url", ""), "log": {}})
    idx[key]["log"][date] = e 


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    for path in glob.glob("collection/log/*/*.json"):
        (date, key) = parse_path(path)
        h = json.load(open(path))
        add(date, key, h)

    save("collection/index.json", canonicaljson.encode_canonical_json(idx))
