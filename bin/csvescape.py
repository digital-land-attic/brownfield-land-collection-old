#!/usr/bin/env python3

#
#  escape newlines in a CSV file
#

import sys
import csv

if __name__ == "__main__":
    writer = csv.writer(sys.stdout)
    for row in csv.reader(sys.stdin):
        row = [s.replace("\r", "").replace("\n", "\\n") for s in row]
        writer.writerow(row)
