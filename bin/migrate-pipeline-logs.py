#!/usr/bin/env python3

import glob
import json
import canonicaljson

for path in glob.glob("collection/log/*/*.json"):
    h = json.load(open(path))

    if "dataset" in h:
        del h["dataset"]

    if "organisation" in h:
        del h["organisation"]

    with open(path, "wb") as f:
        f.write(canonicaljson.encode_canonical_json(h))
