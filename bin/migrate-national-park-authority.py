#!/usr/bin/env python3

import re
import glob
import json
import canonicaljson

for path in glob.glob("collection/log/*/*.json"):
    h = json.load(open(path))

    if "organisation" in h and h["organisation"].startswith("national-park:"):
        h["organisation"] = h["organisation"].replace(
            "national-park:", "national-park-authority:"
        )

    with open(path, "wb") as f:
        f.write(canonicaljson.encode_canonical_json(h))
