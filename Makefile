.PHONY: init sync collection collect validation index clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:
.SUFFIXES: .json

DATASET_NAMES=brownfield-land
DATASET_FILES=dataset/brownfield-land.csv

LOG_FILES=$(wildcard collection/log/*/*.json)
LOG_FILES_TODAY=collection/log/$(shell date +%Y-%m-%d)/

VALIDATION_FILES=$(addsuffix .json,$(subst collection/resource/,validaton/,$(wildcard collection/resource/*)))

all: collection validation

collection: collection/index.json

collect:	$(DATASET_FILES)
	python3 bin/collector.py $(DATASET_NAMES)

collection/index.json: bin/index.py $(DATASET_FILES) collect
	python3 bin/index.py $(DATASET_NAMES)

black:
	black .

clobber::
	rm -rf $(LOG_FILES_TODAY)

init::
	pip3 install --upgrade -r requirements.txt

validation: $(VALIDATION_FILES)

validation/%.json: collection/resource/%
	@mkdir -p validation
	bin/validate.py $< > $@
