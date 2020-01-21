#!/usr/bin/env python3

import sys
import glob
import csv

column = {}

for path in glob.glob("var/normalised/*.csv"):
    reader = csv.DictReader(open(path, newline=""))
    for field in reader.fieldnames:
        column[field] = column.get(field, 0) + 1

    writer = csv.DictWriter(open(sys.argv[1], "w", newline=""), fieldnames=["name", "count"])
    writer.writeheader()
    for name in sorted(column):
        writer.writerow({ "name": name, "count": column[name] })
