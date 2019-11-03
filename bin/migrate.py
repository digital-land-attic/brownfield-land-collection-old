#!/usr/bin/env python3

import re
import glob
import json
import canonicaljson


for path in glob.glob("collection/log/*/*.json"):
    h = json.load(open(path))

    # migrate "body" property to "resource" in headers.json
    h["resource"] = h.pop("body", None)

    with open(path, "wb") as f:
        f.write(canonicaljson.encode_canonical_json(h))
