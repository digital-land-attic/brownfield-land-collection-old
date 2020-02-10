#!/usr/bin/env python

import re
import sys
import json
import csv

schema = json.load(open("schema/brownfield-land.json"))
field_enum = {}
field_value = {}


def normalise_enum_value(value):
    return " ".join(normalise_enum_value.strip.sub(" ", value.lower()).split())


normalise_enum_value.strip = re.compile(r"([^a-z0-9-_ ]+)")


# load enum values from schema
for field in schema["fields"]:
    if "constraints" in field and "enum" in field["constraints"]:
        field_enum.setdefault(field["name"], {})
        for enum in field["constraints"]["enum"]:
            field_enum[field["name"]][normalise_enum_value(enum)] = enum

# load fix-ups from patch file
for row in csv.DictReader(open("patch/enum.csv", newline="")):
    value = normalise_enum_value(row["value"])
    field_value.setdefault(row["field"], {})
    field_value[row["field"]][value] = row["enum"]


writer = csv.DictWriter(sys.stdout, fieldnames=["field", "enum", "value"])
writer.writeheader()

for field in sorted(field_value):
    for value, enum in sorted(field_value[field].items()):
        writer.writerow({"field": field, "enum": enum, "value": value})
