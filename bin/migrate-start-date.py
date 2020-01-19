#!/usr/bin/env python3

import os
import csv
import re

fieldnames = [
    "organisation",
    "documentation-url",
    "resource-url",
    "start-date",
    "end-date",
]

with open("brownfield-land.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for row in csv.DictReader(open("dataset/brownfield-land.csv")):
        if not row["start-date"]:
            m = re.findall(
                r"(2017|2018|2019)[-_]([0-1]\d)[-_]([0-3]\d)", row["resource-url"]
            )
            if m:
                row["start-date"] = "-".join(map(str, m[0]))

        if not row["start-date"]:
            m = re.findall(r"(2017|2018|2019)", row["resource-url"])
            if m:
                # consider adding year ..
                print(row["resource-url"], m)

        writer.writerow(row)
