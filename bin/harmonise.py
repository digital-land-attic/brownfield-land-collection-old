#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#

import os
import sys
import re
import csv
import json
from datetime import datetime
import logging

path = sys.argv[1]
resource = os.path.basename(os.path.splitext(path)[0])

schema = json.load(open("schema/brownfield-land.json"))
fields = {field["name"]: field for field in schema["fields"]}
fieldnames = fields.keys()

pattern = re.compile(r"[^a-z0-9]")


def log_issue(field, fieldtype, value):
    # TBD: log to file for reporting
    logging.info('cannot process %s as a %s: "%s"' % (field, fieldtype, value))


def normalise_date(context, value):
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

    log_issue(field, "date", value)
    return ""


def normalise_uri(field, value):
    # some URIs have line-breaks and spaces
    return "".join(value.split())


def normalise(fieldname, value):
    if value in [None, "", "N/A", "#N/A", "???"]:
        return ""

    field = fields[fieldname]

    if field.get("format", "") == "uri":
        return normalise_uri(fieldname, value)

    if field.get("type", "") == "date":
        return normalise_date(fieldname, value)

    return value


def name(name):
    return re.sub(pattern, "", name.lower())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

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

    reader = csv.DictReader(open(path, newline=""))

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
