#!/usr/bin/env python3

import os
import csv

fieldnames = ["organisation", "documentation-url", "resource-url", "start-date", "end-date"]

with open('brownfield-land.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for row in csv.DictReader(open("dataset/brownfield-land.csv")):
        writer.writerow(row)
