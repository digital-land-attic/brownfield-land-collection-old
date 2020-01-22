#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#

import sys
import re
import csv
import json
from datetime import datetime

schema = json.load(open("schema/brownfield-land.json"))
fields = {field["name"]: field for field in schema["fields"]}
fieldnames = fields.keys()

pattern = re.compile(r"[^a-z0-9]")


def normalise_date(value):
    value = value.strip(' ",')

    # all of these patterns have been used!
    for pattern in [
        "%Y-%m-%d",
        "%Y%m%d",
        "%Y-%m-%dT%H:%M:%S.000Z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y %m %d",
        "%Y.%m.%d",
        "%Y-%d-%m",
        "%Y",
        "%Y.0",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y",
        "%d-%m-%y",
        "%d-%m-%Y",
        "%d.%m.%y",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%m/%d/%Y",
        "%d-%b-%Y",
        "%d-%b-%y",
        "%d %B %Y",
        "%b %d, %Y",
        "%b %d, %y",
        "%b-%y",
    ]:
        try:
            date = datetime.strptime(value, pattern)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return ""


def normalise_uri(value):
    # some URIs have line-breaks and spaces
    return "".join(value.split())


def normalise(fieldname, value):
    if value in [None, "", "N/A", "#N/A", "???"]:
        return ""

    field = fields[fieldname]

    if field.get("format", "") == "uri":
        return normalise_uri(value)

    if field.get("type", "") == "date":
        return normalise_date(value)

    return value


def name(name):
    return re.sub(pattern, "", name.lower())


if __name__ == "__main__":

    # index of typos
    typos = {}
    for fieldname in fieldnames:
        field = fields[fieldname]
        typos[name(fieldname)] = fieldname
        if "title" in field:
            typos[name(field["title"])] = fieldname
        if "digital-land" in field:
            for typo in field["digital-land"].get("typos", []):
                typos[name(typo)] = fieldname

    reader = csv.DictReader(open(sys.argv[1], newline=""))

    # build index of read headers
    headers = {}
    for field in reader.fieldnames:
        if name(field) in typos:
            headers[field] = typos[name(field)]

    with open(sys.argv[2], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            o = {}
            for header in headers:
                field = headers[header]
                o[field] = normalise(field, row[header])

            writer.writerow(o)
