#!/usr/bin/env python3

#
#  create symbolic links for files with a suffix to resources
#
import sys
import os
import os.path
import json


file_dir = "collection/file/"
resource_dir = "../resource/"
index_file = "collection/index.json"


if __name__ == "__main__":
    idx = json.load(open(index_file))
    for resource, r in idx["resource"].items():
        if "suffix" in r:
            link = os.path.join(file_dir, resource + r['suffix'])
            try:
                os.remove(link)
            except:
                pass
            os.symlink(os.path.join(resource_dir, resource), link)
