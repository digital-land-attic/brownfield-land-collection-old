#!/usr/bin/env python3

#
#  normalise CSV file formatting
#

import sys
import csv

data = []

if __name__ == "__main__":
    record = 0
    for row in csv.reader(open(sys.argv[1], newline="")):

        # strip whitespace from fields
        # normalise embedded line endings to CRLF
        row = [v.strip().replace("\r", "").replace("\n", "\r\n") for v in row]

        # skip blank rows
        if "".join(row):
            data.append(row)

    #  TBD: remove blank columns?

    w = csv.writer(open(sys.argv[2], "w", newline=""))
    for row in data:
        w.writerow(row)
