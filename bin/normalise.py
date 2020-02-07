#!/usr/bin/env python3

#
#  normalise CSV file formatting
#

import re
import sys
import csv

spaces = " \n\r\t\f"

null_patterns = []
skip_patterns = []


def skip(row):
    line = ",".join(row)
    for pattern in skip_patterns:
        if pattern.match(line):
            return True
    return False


if __name__ == "__main__":

    # load null patterns
    for row in csv.DictReader(open("patch/null.csv", newline="")):
        null_patterns.append(re.compile(row["pattern"]))

    # load skip patterns
    for row in csv.DictReader(open("patch/skip.csv", newline="")):
        skip_patterns.append(re.compile(row["pattern"]))

    record = 0
    writer = csv.writer(open(sys.argv[2], "w", newline=""))

    for row in csv.reader(open(sys.argv[1], newline="")):

        # strip whitespace and quotes from ends of fields
        # normalise embedded line endings to CRLF
        row = [v.strip(spaces).replace("\r", "").replace("\n", "\r\n") for v in row]

        # strip out fields matching a null pattern
        for pattern in null_patterns:
            row = [pattern.sub("", v) for v in row]

        # skip blank rows
        if not "".join(row):
            continue

        if skip(row):
            continue

        writer.writerow(row)
