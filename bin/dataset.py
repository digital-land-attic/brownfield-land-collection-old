#!/usr/bin/env python3

import os
import sys
import re
import glob
import csv


fieldnames = ["OrganisationURI", "SiteReference" , "GeoX", "GeoY", "Hectares" ,"FirstAddedDate", "LastUpdatedDate", "EndDate"]

#fieldnames = ["organisation", "site" , "latitude", "longitude", "hectares" ,"start-date", "entry-date", "end-date"]

fieldnames.append("resource")


writer = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=fieldnames)
writer.writeheader()

for path in glob.glob(sys.argv[1] + "*.csv"):
    resource = os.path.basename(os.path.splitext(path)[0])

    for row in csv.DictReader(open(path, newline="")):
        row["resource"] = resource
        writer.writerow(row)
