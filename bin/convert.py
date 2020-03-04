#!/usr/bin/env python3

#
#  convert XLS or CSV file into a CSV file encoded in UTF-8
#

import sys
from io import StringIO
from cchardet import UniversalDetector
import csv
import pandas as pd
import logging


def detect_encoding(path):
    detector = UniversalDetector()
    detector.reset()
    with open(path, "rb") as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
    detector.close()
    return detector.result["encoding"]


def from_csv(path):
    encoding = detect_encoding(path)

    if not encoding:
        return None

    logging.debug(f"detected encoding {encoding}")

    with open(path, encoding=encoding, newline="") as f:
        content = f.read()
        if content.lower().startswith("<!doctype "):
            logging.debug(f"{path} has <!doctype")
            return None

        f.seek(0)
        data = []
        for row in csv.reader(f):
            data.append(row)
        return data


def from_excel(path):
    try:
        excel = pd.read_excel(path)
    except:
        return None

    string = excel.to_csv(index=False, header=True, encoding="utf-8", quoting=csv.QUOTE_ALL)

    data = []
    for row in csv.reader(StringIO(string)):
        data.append(row)
    return data


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s"
    )

    path = sys.argv[1]

    data = from_csv(path) or from_excel(path)

    if not data:
        logging.error(f"Unable to convert {path}")
        sys.exit(2)

    csvpath = sys.argv[2]
    logging.debug(f"writing to {csvpath}")
    w = csv.writer(open(sys.argv[2], "w", newline=""))
    for row in data:
        w.writerow(row)
