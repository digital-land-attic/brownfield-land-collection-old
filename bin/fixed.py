#!/usr/bin/env python3

import os
import sys
import glob
import csv

fixed = {}

writer = csv.DictWriter(open(sys.argv[1], "w", newline=""), fieldnames=["resource"])
writer.writeheader()

for path in sorted(glob.glob("fixed/*.csv")):
    resource = os.path.basename(os.path.splitext(path)[0])
    writer.writerow({"resource": resource})
