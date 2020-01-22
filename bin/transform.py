#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#
import os
import sys
import csv
import json


if __name__ == "__main__":

    # TBD: make this a command-line option
    schema = json.load(open("schema/brownfield-land.json"))

    fieldnames = schema["digital-land"]["fields"]
    fields = {
        field["digital-land"]["field"]: field["name"]
        for field in schema["fields"]
        if "digital-land" in field and "field" in field["digital-land"]
    }
    for field in fieldnames:
        if not field in fields:
            fields[field] = field

    path = sys.argv[1]
    resource = os.path.basename(os.path.splitext(path)[0])

    reader = csv.DictReader(open(path, newline=""))

    with open(sys.argv[2], "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            o = {}
            row['resource'] = resource
            row['organisation'] = row["OrganisationURI"]
            for field in fieldnames:
                o[field] = row[fields[field]]

            writer.writerow(o)
