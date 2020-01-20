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

        # skip rows containing 1,2,3,4 ..
        if row == [str(n) for n in range(1, len(row) + 1)]:
            continue

        writer.writerow(row)
