#!/usr/bin/env python3

#
#  transpose CSV
#

import sys
import csv

data = []
for row in csv.reader(open(sys.argv[1], "r", newline="")):
    data.append(row)

writer = csv.writer(open(sys.argv[2], "w", newline=""))
for row in zip(*data):
    writer.writerow(row)
