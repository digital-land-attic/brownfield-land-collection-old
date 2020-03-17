#!/usr/bin/env python3

import csv

organisation = {}

for row in csv.DictReader(open("var/cache/organisation.csv", newline="")):
    organisation[row["organisation"]] = row


w = csv.DictWriter(open("/tmp/enum.csv", "w"), fieldnames=["field", "enum", "value"])
w.writeheader()

for row in csv.DictReader(open("patch/organisation.csv", newline="")):
    w.writerow({"field": "OrganisationURI", "enum": organisation[row["organisation"]]["opendatacommunities"], "value": row["value"]})
