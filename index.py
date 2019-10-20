#!/usr/bin/env python3

#
#  index the collection
#

import re
import glob
import json
from canonicaljson import encode_canonical_json

collection = {"header":{}}


def add(h, category, key):
    collection.setdefault(category, {})
    if category in h:
        collection[category].setdefault(h[category], []).append(key)


p = re.compile("^.*/([\d-]+)/(\w+).json")

for path in glob.glob("collection/headers/*/*.json"):
    date, key = p.match(path).groups()

    h = json.load(open(path))

    for item in ["request-headers", "response-headers"]:
        h.pop(item, None)

    collection["header"][key] = h

    add(h, "dataset", key)
    add(h, "organisation", key)
    add(h, "status", key)
    add(h, "exception", key)

    if "body" in h:
        add(h, "body", key)


with open("index.json", "wb") as f:
    f.write(encode_canonical_json(collection))
