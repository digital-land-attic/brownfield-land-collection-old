.PHONY: init sync collect clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:

TODAYS_HEADERS=collection/headers/$(shell date +%Y-%m-%d)/

all: collect

collect:
	python3 bin/collector.py

black:
	black .

clobber::
	rm -rf $(TODAYS_HEADERS)

init::
	pip3 install -r requirements.txt

