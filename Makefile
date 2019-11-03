.PHONY: init sync collection collect index clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:

TODAYS_HEADERS=collection/headers/$(shell date +%Y-%m-%d)/

all: collect collection

collection: collection/index.json

collect:
	python3 bin/collector.py

collection/index.json: bin/index.py
	python3 bin/index.py

black:
	black .

clobber::
	rm -rf $(TODAYS_HEADERS)

init::
	pip3 install -r requirements.txt

