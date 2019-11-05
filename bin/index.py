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

idx = {
    'resource': {},
    'log': {},
    'url': {},
    'dataset': {},
}

def parse_path(path):
    m = re.match(r"^.*\/([-\d]+)\/(\w+).json", path)
    return m.groups()


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def add(date, key, h):

    idx["url"][key] = h.get("url", "")

    e = {}
    for field in ["status", "exception", "datetime", "elapsed", "resource"]:
        if field in h and h[field]:
            e[field] = h[field]

    idx["log"].setdefault(date, {})
    idx["log"][date][key] = e 

    idx["dataset"].setdefault(h["dataset"], {})
    idx["dataset"][h["dataset"]].setdefault("organisation", {})
    idx["dataset"][h["dataset"]]["organisation"].setdefault(h["organisation"], {})
    idx["dataset"][h["dataset"]]["organisation"][h["organisation"]].setdefault("log", [])
    idx["dataset"][h["dataset"]]["organisation"][h["organisation"]]["log"].append({date : key})


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    for path in glob.glob("collection/log/*/*.json"):
        (date, key) = parse_path(path)
        h = json.load(open(path))
        add(date, key, h)

    save("collection/index.json", canonicaljson.encode_canonical_json(idx))
