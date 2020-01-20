#!/usr/bin/env python3

#
#  normalise CSV file formatting
#

import sys
import csv

if __name__ == "__main__":
    record = 0
    writer = csv.writer(open(sys.argv[2], "w", newline=""))

    for row in csv.reader(open(sys.argv[1], newline="")):

        # strip whitespace from fields
        # normalise embedded line endings to CRLF
        row = [v.strip().replace("\r", "").replace("\n", "\r\n") for v in row]

        # skip blank rows
        if not "".join(row):
            continue

        line = ",".join(row)

        # skip sequence numbered rows
        if line.startswith("1,2,3,4,5,6,7,8,"):
            continue

        # skip rows containing a lot of Unnamed values
        # possibly too aggressive?
        if row[0] == "Unnamed: 0":
            continue

        if "Unnamed: 1,Unnamed: 2,Unnamed: 3,Unnamed: 4" in line:
            continue

        # skip common notes row
        if "Mandatory,Mandatory,Mandatory,Mandatory,Mandatory,Mandatory,Mandatory" in line:
            continue

        writer.writerow(row)
