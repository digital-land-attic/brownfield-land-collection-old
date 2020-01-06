#!/usr/bin/env python3

#
#  fix obvious issues in a brownfield land CSV
#  -- make it valid according to the 2019 guidance
#  -- log fixes as suggestions for the user to amend
#
import os
import logging
import csv

rows = []

def load(path):
    with open(path, newline='') as f:
        for row in csv.reader(f):
            rows.append(row)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    #load('var/csv/000b261f1757b69b9435ec20bae8f2b141677d17c054f01b187c8952e117db33.csv')

    # spaces in titles
    #load('var/csv/47ae15c373da005ad5d1280e13163dca5725ed4a04b32374991d14004b9eab78.csv')

    # UPPERCASE TITLES
    load('var/csv/3875c4aecb090ce1db8446c0b3f56a90628d8dba570b230767c29b74fcf79b35.csv')
    print(rows)
