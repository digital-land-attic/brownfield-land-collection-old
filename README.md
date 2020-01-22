# Digital Land brownfield land collection

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/digital-land/brownfield-land/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

Collect data published by each Local Planning Authority, validate the publications, and build a national [dataset](dataset).

# Collection

The source list of registers collected is kept and maintained in [dataset/brownfield-land.csv](dataset/brownfield-land.csv).

The [collection](collection) directory contains resources collected from sources:

* [collection/log](collection/log) -- log entries by date (sha256 hash of the URL)
* [collection/resource](collection/resource) -- collected files (sha256 of the contents)

# Validation

Each collected resource is processed, creating a file with the same basename as the resource in the following directories:

* [validation](validation) -- validation results for each resource as JSON

# Processing pipeline

The collected resources are then processed in the following pipeline:

* [var/converted](var/converted) -- the resource converted into UTF-8 encoded CSV
* [var/normalised](var/normalised) -- removed padding, drop obviously spurious rows
* [var/harmonised](var/harmonised) -- dates, geospatial, and other values translated into a consistent format
* [var/transformed](var/transformed) -- transformed into the digital-land dataset model

# Indexes

The collection is then collated into a register for each organisation, and a national dataset:

* [index/dataset.csv](index/dataset.csv)

A number of index files are generated for the collection:

* [index/link.csv](index/link.csv) -- url, link (hash)
* [index/log.csv](index/log.csv) -- datetime, link, resource, HTTP status, content-type, elapsed time
* [index/resource.csv](index/resource.csv) -- resource (hash), media-type, suffix, row-count, error-count
* [collection/index.json](collection/index.json) -- the entire index in a single JSON file

These indexes are used by the [dataset](https://github.com/digital-land/brownfield-land/) and other code to build the [dataset](https://digital-land.github.io/dataset/brownfield-land/), [resource](https://digital-land.github.io/resource/), and other pages.

# Manually fixed files

Resources which are PDF documents or other formats which cannot be processable are fixed by the team:
hand, and are introduced into the pipeline instead of the collected resource:

* [fixed](fixed) -- manually fixed resources

# Updating the collection

We recommend working in [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) before installing the python dependencies:

    $ make init
    $ make

Not all of the files can be downloaded automatically. These can be added to the collection using the [addone](bin/addone.py) script;

    $ bin/addone.py ~/Downloads/download.csv https://example.com/inaccessible-site

# Licence

The software in this project is open source and covered by LICENSE file.

Individual datasets copied into this repository may have specific copyright and licensing, otherwise all content and data in this repository is
[© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/)
and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
