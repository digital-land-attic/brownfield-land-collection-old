.PHONY: init collection collect second-pass normalise validate harmonise transform index clobber black clean prune
.SECONDARY:
.DELETE_ON_ERROR:
.SUFFIXES: .json

RESOURCE_DIR=collection/resource/
FIXED_DIR=fixed/

VALIDATION_DIR=validation/
CONVERTED_DIR=var/converted/
NORMALISED_DIR=var/normalised/
HARMONISED_DIR=var/harmonised/
TRANSFORMED_DIR=var/transformed/

DATASET_NAME=brownfield-land
DATASET_FILES=dataset/$(DATASET_NAME).csv
SCHEMA=schema/$(DATASET_NAME).json

LOG_FILES:=$(wildcard collection/log/*/*.json)
LOG_FILES_TODAY:=collection/log/$(shell date +%Y-%m-%d)/

# validation targets
VALIDATION_FILES:=$(addsuffix .json,$(subst $(RESOURCE_DIR),$(VALIDATION_DIR),$(RESOURCE_FILES)))

# sources
RESOURCE_FILES:=$(wildcard $(RESOURCE_DIR)*)
FIXED_FILES:=$(wildcard $(FIXED_DIR)*.csv)
FIXED_CONVERTED_FILES:=$(subst $(FIXED_DIR),$(CONVERTED_DIR),$(FIXED_FILES))

# pipeline targets
CONVERTED_FILES:=$(addsuffix .csv,$(subst $(RESOURCE_DIR),$(CONVERTED_DIR),$(RESOURCE_FILES)))
NORMALISED_FILES:=$(subst $(CONVERTED_DIR),$(NORMALISED_DIR),$(CONVERTED_FILES))
HARMONISED_FILES:=$(subst $(CONVERTED_DIR),$(HARMONISED_DIR),$(CONVERTED_FILES))
TRANSFORMED_FILES:=$(subst $(CONVERTED_DIR),$(TRANSFORMED_DIR),$(CONVERTED_FILES))

# generated dataset
NATIONAL_DATASET=index/dataset.csv

# indexes
COLLECTION_INDEXES=\
	collection/index.json\
	index/link.csv\
	index/log.csv\
	index/resource.csv\

INDEXES=\
	$(COLLECTION_INDEXES)\
	index/fixed.csv\
	index/column.csv

TBD_COLLECTION_INDEXES=\
	index/organisation-documentation.csv\
	index/organisation-link.csv\
	index/organisation-resource.csv\

BROKEN_VALIDATIONS=\
	validation/7ba205f5d2619398a931669c1e6d4c8850f6fbefe2d6838a3ebbbe5f9200b702.json\
	validation/9155144a6fefb61252f68c817b8e2050c14e10072260cd985f53cb74c09a4650.json


all: collect second-pass


collect:	$(DATASET_FILES)
	python3 bin/collector.py $(DATASET_NAME)

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

index: $(INDEXES)
	@:

dataset: $(NATIONAL_DATASET)
	@:

#
#  indexes
#
$(NATIONAL_DATASET): bin/dataset.py $(TRANSFORMED_FILES) $(SCHEMA)
	python3 bin/dataset.py $(TRANSFORMED_DIR) $@

$(COLLECTION_INDEXES): bin/index.py $(DATASET_FILES) $(LOG_FILES) $(VALIDATION_FILES)
	python3 bin/index.py $(DATASET_NAME)

index/column.csv: bin/columns.py $(NORMALISED_FILES)
	python3 bin/columns.py $@

index/fixed.csv: bin/fixed.py $(FIXED_FILES)
	python3 bin/fixed.py $@

#
#  validation
#  -- depends on schema
#  -- but this is expensive to rebuild during development
#
#$(VALIDATION_DIR)%.json: $(RESOURCE_DIR)% $(SCHEMA)
$(VALIDATION_DIR)%.json: $(RESOURCE_DIR)%
	@mkdir -p $(VALIDATION_DIR)
	validate --exclude-input --exclude-rows --file $< --output $@

#
#  pipeline to build national dataset
#
$(CONVERTED_DIR)%.csv: $(RESOURCE_DIR)% bin/convert.py
	@mkdir -p $(CONVERTED_DIR)
	python3 bin/convert.py $< $@

$(NORMALISED_DIR)%.csv: $(CONVERTED_DIR)%.csv bin/normalise.py
	@mkdir -p $(NORMALISED_DIR)
	python3 bin/normalise.py $< $@

$(HARMONISED_DIR)%.csv: $(NORMALISED_DIR)%.csv bin/harmonise.py $(SCHEMA)
	@mkdir -p $(HARMONISED_DIR)
	python3 bin/harmonise.py $< $@

$(TRANSFORMED_DIR)%.csv: $(HARMONISED_DIR)%.csv bin/transform.py $(SCHEMA)
	@mkdir -p $(TRANSFORMED_DIR)
	python3 bin/transform.py $< $@

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
