#!/usr/bin/env python3

#
#  normalise CSV file formatting
#

import re
import sys
import csv

spaces = " \n\r\t\f"

patterns = []


def skip(row):
    line = ",".join(row)
    for pattern in patterns:
        if pattern.match(line):
            return True
    return False


if __name__ == "__main__":

    # load skip patterns
    for row in csv.DictReader(open("patch/skip.csv", newline="")):
        patterns.append(re.compile(row["pattern"]))

    record = 0
    writer = csv.writer(open(sys.argv[2], "w", newline=""))

    for row in csv.reader(open(sys.argv[1], newline="")):

        # strip whitespace and quotes from ends of fields
        # normalise embedded line endings to CRLF
        row = [v.strip(spaces).replace("\r", "").replace("\n", "\r\n") for v in row]

        # skip blank rows
        if not "".join(row):
            continue

        if skip(row):
            continue

        writer.writerow(row)
