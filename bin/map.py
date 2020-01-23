#!/usr/bin/env python3

#
#  fix field names using the provide schema
#

import os
import sys
import re
import csv
import json

input_path = sys.argv[1]
output_path = sys.argv[2]
schema_path = sys.argv[3]

schema = json.load(open(schema_path))
fields = {field["name"]: field for field in schema["fields"]}
fieldnames = [field["name"] for field in schema["fields"]]

pattern = re.compile(r"[^a-z0-9]")


def name(name):
    return re.sub(pattern, "", name.lower())


if __name__ == "__main__":
    # index of fieldname typos
    typos = {}
    for fieldname in fieldnames:
        field = fields[fieldname]
        typos[name(fieldname)] = fieldname
        if "title" in field:
            typos[name(field["title"])] = fieldname
        if "digital-land" in field:
            for typo in field["digital-land"].get("typos", []):
                typos[name(typo)] = fieldname

    reader = csv.DictReader(open(input_path, newline=""))

    # build index of headers from the input
    headers = {}
    for field in reader.fieldnames:
        if name(field) in typos:
            headers[field] = typos[name(field)]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            o = {}
            for header in headers:
                field = headers[header]
                o[field] = row[header]

            writer.writerow(o)
