#!/usr/bin/env python3

#
#  create an index for a collection
#
import os
from sys import argv
import re
import glob
from datetime import datetime
import validators
import logging
import hashlib
import csv
import json
import canonicaljson

dataset_dir = "dataset/"
log_dir = "collection/log/"
resource_dir = "collection/resource/"
idx = {}
resources = {}


def parse_log_path(path):
    m = re.match(r"^.*\/([-\d]+)\/(\w+).json", path)
    return m.groups()


def parse_resource_path(path):
    m = re.match(r"^.*\/(\w+)$", path)
    return m.groups()[0]


def valid_url(n, url):
    if url != "" and not validators.url(url):
        logging.error("line %d: invalid url %s" % (n, url))


def valid_date(n, date):
    if date != "" and date != datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d"):
        logging.error("line %d: invalid date %s" % (n, date))


def valid_data_gov_uk(n, s):
    if s != "" and not re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", s):
        logging.error("line %d: invalid data.gov.uk id %s" % (n, s))


def save(path, data):
    logging.info(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def load(dataset):
    n = 1
    for row in csv.DictReader(open(os.path.join(dataset_dir, dataset + ".csv"))):
        n += 1
        valid_url(n, row["documentation-url"])
        valid_url(n, row["resource-url"])
        valid_data_gov_uk(n, row["data-gov-uk"])
        valid_date(n, row["start-date"])
        valid_date(n, row["end-date"])

        key = hashlib.sha256(row["resource-url"].encode("utf-8")).hexdigest()
        idx.setdefault(key, {"url": row.get("resource-url", ""), "log": {}, "organisation": {}})
        idx[key]["organisation"].setdefault(row["organisation"], {})
        for field in ["documentation-url", "data-gov-uk", "start-date", "end-date", "esd-dataset"]:
            if row[field]:
                idx[key]["organisation"][row["organisation"]][field] = row[field]


def add(path, date, key, h):
    if not h.get("url", ""):
        logging.error("no url for %s/%s" % (date, key))

    # check key in log filename matches url
    _key = hashlib.sha256(h["url"].encode("utf-8")).hexdigest()
    if key != _key:
        logging.warning("incorrect key for %s expected %s in %s" % (h["url"], _key, path))
        key, _key = _key, key

    e = {}
    for field in ["status", "exception", "datetime", "elapsed", "resource"]:
        if field in h and h[field]:
            e[field] = h[field]

    if h.get("status", "") == "200" and "response-headers" in h:
        for field in ["Content-Type", "Content-Length"]:
            if field in h["response-headers"]:
                e[field] = h["response-headers"][field]

    if "resource" in e:
        resources.setdefault(e["resource"], True)

    if key not in idx:
        logging.error("no dataset entry for: %s %s cited in path" % (h["url"], key, path))
        idx.setdefault(key, {"url": h["url"], "log": {}})

    # avoid date collisions with a valid key
    while date in idx[key]["log"]:
        date += "⚠"

    idx[key]["log"][date] = e


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    # load datasets
    for dataset in argv[1:]:
        load(dataset)

    # process log files
    for path in glob.glob("%s*/*.json" % (log_dir)):
        (date, key) = parse_log_path(path)
        h = json.load(open(path))
        add(path, date, key, h)

    # check resource files are in the log
    for path in glob.glob("%s*" % (resource_dir)):
        resource = parse_resource_path(path)
        if resource in resources:
            resources[resource] = False
        else:
            logging.error("no log for path" % (path))

    # check resources in the log exist as files
    for resource in resources:
        if resources[resource]:
            logging.error("missing resource: %s" % (resource))

    save("collection/index.json", canonicaljson.encode_canonical_json(idx))
