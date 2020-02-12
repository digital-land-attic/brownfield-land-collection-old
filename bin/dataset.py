#!/usr/bin/env python3

#
#  turn sorted entries into latest records
#

import os
import sys
import re
import glob
import csv
import json

keys = {}

if __name__ == "__main__":

    reader = csv.DictReader(open(sys.argv[1], newline=""))

    writer = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        key = ("%s:%s" % (row["organisation"], row["site"]))
        if key not in keys:
            writer.writerow(row)
            keys[key] = True
