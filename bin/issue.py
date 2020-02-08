#!/usr/bin/env python3

import os
import sys
import glob
import csv

log_fieldnames = ["resource", "row-number", "field", "issue-type", "value"]

writer = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=log_fieldnames)
writer.writeheader()

for path in sorted(glob.glob(sys.argv[1] + "*.csv")):
    resource = os.path.basename(os.path.splitext(path)[0])

    for row in csv.DictReader(open(path, newline="")):
        row["resource"] = resource
        writer.writerow(row)
