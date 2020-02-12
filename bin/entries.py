#!/usr/bin/env python3

#
#  assemble files into a single dataset of entries
#

import os
import sys
import re
import glob
import csv
import json

resource_date = {}
entries = []

if __name__ == "__main__":

    for row in csv.DictReader(open("index/resource-organisation.csv", newline="")):
        resource_date[row["resource"]] = row["start-date"]

    for path in sorted(glob.glob(sys.argv[1] + "*.csv")):
        for row in csv.DictReader(open(path, newline="")):
            row["resource-date"] = resource_date[row["resource"]]
            entries.append(row)

    schema = json.load(open("schema/brownfield-land.json"))
    fieldnames = ["resource-date"] + schema["digital-land"]["fields"]

    writer = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=fieldnames)
    writer.writeheader()

    for row in sorted(entries, key=lambda e: (e['resource-date'], e["entry-date"], e["organisation"], e["site"])):
        writer.writerow(row)
