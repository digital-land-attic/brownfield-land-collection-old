# Digital Land brownfield land collection

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/digital-land/brownfield-land/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

Collect data published by each Local Planning Authority, validate the publications, and build a national [dataset](https://digital-land.github.io/dataset/brownfield-land/).

You can explore data with a geospatial position on our [map](https://digital-land.github.io/map/).

# Collection

The source list of registers collected is kept and maintained in [dataset/brownfield-land.csv](dataset/brownfield-land.csv).

The [collection](collection) directory contains resources collected from sources:

* [collection/log](collection/log) -- log entries by date (sha256 hash of the URL)
* [collection/resource](collection/resource) -- collected files (sha256 of the contents)

# Processing pipeline

The collected resources are then processed in a pipeline:

* [var/converted](var/converted) -- the resource converted into UTF-8 encoded CSV
* [var/normalised](var/normalised) -- removed padding, drop obviously spurious rows
* [var/mapped](var/mapped) -- column names mapped to ones in the schema
* [var/harmonised](var/harmonised) -- dates, geospatial, and other values translated into a consistent format
* [var/transformed](var/transformed) -- transformed into the digital-land dataset model

# Dataset

The resources are then collated into a national set of entries, ordered by the date the resource was published, and the entry-date:

* [index/entries.csv](index/entries.csv)

The entries are then reduced to a national dataset of site records, using the organisation and site reference to uniquely identify a site, and the order of the entries to help remove duplicate and older entries:

* [index/dataset.csv](index/dataset.csv)


which has the following fields, to be consistent with other datasets published by digital land:

* entry-date
* organisation -- the curie for the organisation
* site -- a unique identifier for the site
* site-address
* site-plan-url
* deliverable
* ownership
* planning-permission-status
* planning-permission-type
* hazardous-substances
* latitude
* longitude
* hectares
* minimum-net-dwellings
* maximum-net-dwellings
* start-date
* end-date
* resource -- the source resource for the entry

# Indexes

A number of index files are generated for the collection:

* [index/link.csv](index/link.csv) -- url, link (hash)
* [index/log.csv](index/log.csv) -- datetime, link, resource, HTTP status, content-type, elapsed time
* [index/resource.csv](index/resource.csv) -- resource (hash), media-type, suffix, row-count, error-count
* [index/issue.csv](index/issue.csv) -- resource, row-number, field and value which can't be processed
* [index/column.csv](index/column.csv) -- count of the column names found in normalised files
* [index/index.json](collection/index.json) -- an index of the collection in a single JSON file

These indexes are used by the [dataset](https://github.com/digital-land/brownfield-land/) and other code to build the [dataset](https://digital-land.github.io/dataset/brownfield-land/), [resource](https://digital-land.github.io/resource/), and other pages.

# Manual fixes

Resources which cannot be automatically processed are fixed manually using the following configuration and data:

* [fixed](fixed) -- manually fixed resources introduced into the pipeline instead of the collected resource
* [patches/organisation.csv](patches/organisation) -- a map of OrganisationURI to organisation CURIE values

# Validation

Each collected resource is tested for conformance to the [schema](schema/brownfield-land.json) which is a [frictionless data schema](https://frictionlessdata.io/specs/table-schema/) with extensions to support the pipeline. The results of validation are stored in the [validation](validation) directory, and included in the indexes.

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
