#!/usr/bin/env python3

import re
import glob
import json
import canonicaljson

organisation = {
    "development-corporation:1": "development-corporation:Q6670544",
    "development-corporation:2": "development-corporation:Q20648596",
    "national-park:1": "national-park:Q72617988",
    "national-park:10": "national-park:Q72618127",
    "national-park:2": "national-park:Q27159704",
    "national-park:3": "national-park:Q5225646",
    "national-park:4": "national-park:Q72617669",
    "national-park:5": "national-park:Q27178932",
    "national-park:6": "national-park:Q72617784",
    "national-park:7": "national-park:Q72617890",
    "national-park:8": "national-park:Q4972284",
    "national-park:9": "national-park:Q72617158",
}

for path in glob.glob("collection/log/*/*.json"):
    h = json.load(open(path))

    # migrate "body" property to "resource" in headers.json
    if "body" in h and "resource" not in h:
        h["resource"] = h.pop("body", None)

    # move development corporations and national parks to wikidata based scheme
    if "organisation" in h and h["organisation"] in organisation:
        h["organisation"] = organisation[h["organisation"]]

    with open(path, "wb") as f:
        f.write(canonicaljson.encode_canonical_json(h))
