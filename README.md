# Digital Land brownfield land collection

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/digital-land/brownfield-land/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

Collect brownfield land register data from each Local Planning Authority, validate the data, and build a national dataset.

The source list of registers collected is kept and maintained in [dataset/brownfield-land.csv](dataset/brownfield-land.csv).

The [collection](collection) directory contains:

* [collection/log](collection/log) -- log entries by date (sha256 hash of the URL)
* [collection/resource](collection/resource) -- collected files (sha256 of the contents)
* [index.json](collection/index.json) -- an index into the collection, used to build [dataset](https://digital-land.github.io/dataset/brownfield-land/) and other pages

The [validation](validation) directory contains the results of validating each resource as JSON.

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
