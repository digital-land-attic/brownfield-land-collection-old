#!/usr/bin/env python3

#
#  assemble files into a single dataset
#

import os
import sys
import re
import glob
import csv
import json


if __name__ == "__main__":

    schema = json.load(open("schema/brownfield-land.json"))
    fieldnames = schema["digital-land"]["fields"]

    writer = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=fieldnames)
    writer.writeheader()

    for path in sorted(glob.glob(sys.argv[1] + "*.csv")):
        resource = os.path.basename(os.path.splitext(path)[0])

        for row in csv.DictReader(open(path, newline="")):
            row["resource"] = resource
            writer.writerow(row)
