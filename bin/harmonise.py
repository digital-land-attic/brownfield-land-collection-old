#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#

import sys
import re
import csv

# TBD: load full schema.json
schema = {
    "fields": [
        {
            "name": "OrganisationURI",
            "title": "Organisation URI",
            "description": "The URL of the organisation on https://opendatacommunities.org",
            "type": "string",
            "format": "uri",
            "constraints": {
                "required": True
            },
            "typos": [ "OrganistionURI" ]
        },
    ]
}

pattern = re.compile(r'[^a-z0-9]')


def name(name):
    return re.sub(pattern, '', name.lower())


if __name__ == "__main__":

    fieldnames = [field["name"] for field in schema["fields"]]

    # index of typos
    typos = {}
    for field in schema["fields"]:
        typos[name(field["title"])] = field["name"]
        for typo in field["typos"]:
            typos[name(typo)] = field["name"]

    reader = csv.DictReader(open(sys.argv[1], newline=""))

    # build index of read headers
    headers = {}
    for field in reader.fieldnames:
        if name(field) in typos:
            headers[field] = typos[name(field)]

    print("reader.fieldnames", reader.fieldnames)
    print("headers", headers)

    with open(sys.argv[2], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            o = {}
            for header in headers:
                o[headers[header]] = row[header]

            writer.writerow(o)
