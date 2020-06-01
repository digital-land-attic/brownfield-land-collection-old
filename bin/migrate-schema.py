#!/usr/bin/env python

import re
import sys
import json
import csv

schema = json.load(open("schema/brownfield-land.json"))


datatypes = set()
fields = []

from pprint import pprint

for field in schema["fields"]:
    datatypes.add(field.get("type", None))
    fields.append(
        {
            "name": field["name"],
            "datatype": field.get("type", None),
            "description": field["description"],
            "parent-field": "",
            "replacement-field": "",
        }
    )

with open("schema/schema.csv", "w") as schema_file:
    schema_csv = csv.DictWriter(schema_file, fieldnames=["name", "field"])
    schema_csv.writeheader()
    schema_csv.writerow({"name": "Brownfield Land", "field": "brownfield-land"})
print(f"1 schema written to schema/schema.csv")

schema_field_count = 0
with open("schema/schema-field.csv", "w") as schema_field_file:
    schema_field_csv = csv.DictWriter(
        schema_field_file,
        fieldnames=["schema", "field", "cardinality", "description",],
    )
    schema_field_csv.writeheader()
    for field in fields:
        schema_field_csv.writerow(
            {
                "schema": "brownfield-land",
                "field": field["name"],
                "cardinality": "",
                "description": field["description"],
            }
        )
        schema_field_count += 1
print(f"{schema_field_count} schema fields written to schema/schema-field.csv")

field_count = 0
with open("schema/field.csv", "w") as field_file:
    field_csv = csv.DictWriter(
        field_file,
        fieldnames=[
            "name",
            "datatype",
            "description",
            "parent-field",
            "replacement-field",
        ],
    )
    field_csv.writeheader()
    for field in fields:
        field_csv.writerow(field)
        field_count += 1
print(f"{field_count} fields written to schema/field.csv")


datatype_count = 0
with open("schema/datatype.csv", "w") as datatype_file:
    datatype_csv = csv.DictWriter(datatype_file, fieldnames=["name"])
    datatype_csv.writeheader()
    for datatype in datatypes:
        datatype_csv.writerow({"name": datatype})
        datatype_count += 1
print(f"{datatype_count} datatypes written to schema/datatype.csv")
