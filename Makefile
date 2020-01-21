.PHONY: init collection collect second-pass normalise validate harmonise index clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:
.SUFFIXES: .json

RESOURCE_DIR=collection/resource/
FIXED_DIR=fixed/

VALIDATION_DIR=validation/
CONVERTED_DIR=var/converted/
NORMALISED_DIR=var/normalised/
HARMONISED_DIR=var/harmonised/

DATASET_NAMES=brownfield-land
DATASET_FILES=dataset/brownfield-land.csv

LOG_FILES:=$(wildcard collection/log/*/*.json)
LOG_FILES_TODAY:=collection/log/$(shell date +%Y-%m-%d)/

RESOURCE_FILES:=$(wildcard $(RESOURCE_DIR)*)
FIXED_FILES:=$(wildcard $(FIXED_DIR)*.csv)
FIXED_CONVERTED_FILES:=$(subst $(FIXED_DIR),$(CONVERTED_DIR),$(FIXED_FILES))
VALIDATION_FILES:=$(addsuffix .json,$(subst $(RESOURCE_DIR),$(VALIDATION_DIR),$(RESOURCE_FILES)))
CONVERTED_FILES:=$(addsuffix .csv,$(subst $(RESOURCE_DIR),$(CONVERTED_DIR),$(RESOURCE_FILES)))
NORMALISED_FILES:=$(subst $(CONVERTED_DIR),$(NORMALISED_DIR),$(CONVERTED_FILES))
HARMONISED_FILES:=$(subst $(NORMALISED_DIR),$(HARMONISED_DIR),$(NORMALISED_FILES))

NATIONAL_DATASET=index/dataset.csv

COLLECTION_INDEX=\
	collection/index.json\
	index/link.csv\
	index/log.csv\
	index/resource.csv\

INDEXES=\
	index/column.csv

TBD_COLLECTION_INDEX=\
	index/organisation-documentation.csv\
	index/organisation-link.csv\
	index/organisation-resource.csv\

BROKEN_VALIDATIONS=\
	validation/7ba205f5d2619398a931669c1e6d4c8850f6fbefe2d6838a3ebbbe5f9200b702.json\
	validation/9155144a6fefb61252f68c817b8e2050c14e10072260cd985f53cb74c09a4650.json


all: collect second-pass


collect:	$(DATASET_FILES)
	python3 bin/collector.py $(DATASET_NAMES)

# restart the make process to pick-up collected files
second-pass:
	@make --no-print-directory validate harmonise index dataset


validate: $(VALIDATION_FILES)
	@:

convert: $(CONVERTED_FILES)
	@:

normalise: $(NORMALISED_FILES)
	@:

harmonise: $(HARMONISED_FILES)
	@:

index: $(COLLECTION_INDEX) $(INDEXES)
	@:

dataset: $(NATIONAL_DATASET)
	@:

$(COLLECTION_INDEX): bin/index.py $(DATASET_FILES) $(LOG_FILES) $(VALIDATION_FILES)
	python3 bin/index.py brownfield-land

$(NATIONAL_DATASET): bin/dataset.py $(HARMONISED_FILES)
	python3 bin/dataset.py $(HARMONISED_DIR) $@

index/column.csv: bin/columns.py $(NORMALISED_FILES)
	python3 bin/columns.py $@

#
#  pipeline to build national dataset
#
$(VALIDATION_DIR)%.json: $(RESOURCE_DIR)%
	@mkdir -p $(VALIDATION_DIR)
	validate --exclude-input --exclude-rows --file $< --output $@

$(CONVERTED_DIR)%.csv: $(RESOURCE_DIR)% bin/convert.py
	@mkdir -p $(CONVERTED_DIR)
	python3 bin/convert.py $< $@

$(NORMALISED_DIR)%.csv: $(CONVERTED_DIR)%.csv bin/normalise.py
	@mkdir -p $(NORMALISED_DIR)
	python3 bin/normalise.py $< $@

$(HARMONISED_DIR)%.csv: $(NORMALISED_DIR)%.csv bin/harmonise.py schema/brownfield-land.json
	@mkdir -p $(HARMONISED_DIR)
	python3 bin/harmonise.py $< $@


# hand-fixes for resources which can't be processed
$(FIXED_CONVERTED_FILES):
	@mkdir -p $(CONVERTED_DIR)
	python3 bin/convert.py $(subst $(CONVERTED_DIR),$(FIXED_DIR),$@) $@

# fix validation which the validator fails on ..
$(BROKEN_VALIDATIONS):
	@mkdir -p $(VALIDATION_DIR)
	echo '{ "meta_data": {}, "result": {"tables":[{}]} }' > $@


black:
	black .

clobber::
	rm -rf $(LOG_FILES_TODAY)

init::
	pip3 install --upgrade -r requirements.txt

prune:
	rm -rf ./var $(VALIDATION_DIR)
