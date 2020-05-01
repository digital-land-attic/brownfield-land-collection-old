.PHONY: init collection collect second-pass normalise validate harmonise transform index dataset clear-cache clobber clobber-today black clean prune
.SECONDARY:
.DELETE_ON_ERROR:
.SUFFIXES: .json

# work in UTF-8
LANGUAGE := en_GB.UTF-8
LANG := C.UTF-8

# for consistent collation
LC_COLLATE := C.UTF-8

DATASET_NAME=brownfield-land

RESOURCE_DIR=collection/resource/
VALIDATION_DIR=validation/

# fixes and patches
FIXED_DIR=fixed/
PATCH_DIR=patch/

# generated files
INDEX_DIR=index/
COUNT_DIR=index/count/

# intermediate files
CACHE_DIR=var/cache
CONVERTED_DIR=var/converted/
NORMALISED_DIR=var/normalised/
MAPPED_DIR=var/mapped/
HARMONISED_DIR=var/harmonised/
ISSUE_DIR=var/issue/
TRANSFORMED_DIR=var/transformed/
TMP_DIR=tmp/

# data sources
DATASET_FILES=dataset/$(DATASET_NAME).csv

# schema for collected files, and transformation pipeline
SCHEMA=schema/$(DATASET_NAME).json

# collection log
LOG_FILES:=$(wildcard collection/log/*/*.json)
LOG_FILES_TODAY:=collection/log/$(shell date +%Y-%m-%d)/

# collected resources
RESOURCE_FILES:=$(wildcard $(RESOURCE_DIR)*)

# validation targets
VALIDATION_FILES:=$(addsuffix .json,$(subst $(RESOURCE_DIR),$(VALIDATION_DIR),$(RESOURCE_FILES)))

# files which break the validator
BROKEN_VALIDATIONS=\
	validation/7ba205f5d2619398a931669c1e6d4c8850f6fbefe2d6838a3ebbbe5f9200b702.json\
	validation/9155144a6fefb61252f68c817b8e2050c14e10072260cd985f53cb74c09a4650.json

# files which can't be converted
FIXED_FILES:=$(wildcard $(FIXED_DIR)*.csv)
FIXED_CONVERTED_FILES:=$(subst $(FIXED_DIR),$(CONVERTED_DIR),$(FIXED_FILES))

# pipeline targets
CONVERTED_FILES  := $(addsuffix .csv,$(subst $(RESOURCE_DIR),$(CONVERTED_DIR),$(RESOURCE_FILES)))
NORMALISED_FILES := $(subst $(CONVERTED_DIR),$(NORMALISED_DIR),$(CONVERTED_FILES))
MAPPED_FILES     := $(subst $(CONVERTED_DIR),$(MAPPED_DIR),$(CONVERTED_FILES))
HARMONISED_FILES := $(subst $(CONVERTED_DIR),$(HARMONISED_DIR),$(CONVERTED_FILES))
ISSUE_FILES := $(subst $(CONVERTED_DIR),$(ISSUE_DIR),$(CONVERTED_FILES))
TRANSFORMED_FILES:= $(subst $(CONVERTED_DIR),$(TRANSFORMED_DIR),$(CONVERTED_FILES))

# data needed for normalisation
NORMALISE_DATA:=\
	$(PATCH_DIR)/null.csv\
	$(PATCH_DIR)/skip.csv

# data needed for harmonisation
#
# used by broken resources:
# $(INDEX_DIR)/resource-organisation.csv
#
HARMONISE_DATA=\
	$(CACHE_DIR)/organisation.csv\
	$(PATCH_DIR)/OrganisationURI.csv\
	$(PATCH_DIR)/enum.csv

# generated indexes
# TBD: replace with sqlite3
COLLECTION_INDEX=\
	$(INDEX_DIR)/index.json

COLLECTION_INDEXES=\
	$(INDEX_DIR)log.csv\
	$(INDEX_DIR)link.csv\
	$(INDEX_DIR)link-resource.csv\
	$(INDEX_DIR)link-organisation.csv\
	$(INDEX_DIR)resource.csv\
	$(INDEX_DIR)resource-organisation.csv

DATASET_INDEXES=\
	$(INDEX_DIR)organisation-documentation.csv\
	$(INDEX_DIR)organisation-link.csv

PIPELINE_INDEXES=\
	$(INDEX_DIR)fixed.csv\
	$(INDEX_DIR)issue.csv

COUNTS=\
	$(COUNT_DIR)column.csv\
	$(COUNT_DIR)OrganisationURI.csv\
	$(COUNT_DIR)OrganisationLabel.csv\
	$(COUNT_DIR)OwnershipStatus.csv\
	$(COUNT_DIR)HazardousSubstances.csv\
	$(COUNT_DIR)PlanningStatus.csv\
	$(COUNT_DIR)PermissionType.csv\
	$(COUNT_DIR)Deliverable.csv

INDEXES=\
	$(COLLECTION_INDEX)\
	$(COLLECTION_INDEXES)\
	$(PIPELINE_INDEXES)\
	$(COUNTS)

# dataset of mapped files
MAPPED_DATASET=$(TMP_DIR)mapped.csv

# national dataset entries
NATIONAL_DATASET_ENTRIES=$(INDEX_DIR)entries.csv

# national dataset latest entries (records)
NATIONAL_DATASET_RECORDS=$(INDEX_DIR)dataset.csv

all: collect second-pass

collect:	$(DATASET_FILES)
	python3 bin/collector.py $(DATASET_NAME)

# restart the make process to pick-up collected files
second-pass:
	@$(MAKE) --no-print-directory validate harmonise dataset index

validate: $(VALIDATION_FILES)
	@:

convert: $(CONVERTED_FILES)
	@:

normalise: $(NORMALISED_FILES)
	@:

map: $(MAPPED_FILES)
	@:

harmonise: $(COLLECTION_INDEX) $(HARMONISED_FILES)
	@:

entries: $(NATIONAL_DATASET_ENTRIES) $(TRANSFORMED_FILES)
	@:

dataset: $(NATIONAL_DATASET_RECORDS)
	@:

index: $(INDEXES)
	@:

#
#  collection indexes
#
$(NATIONAL_DATASET_RECORDS): bin/dataset.py $(NATIONAL_DATASET_ENTRIES) $(SCHEMA)
	@mkdir -p $(INDEX_DIR)
	python3 bin/dataset.py $(NATIONAL_DATASET_ENTRIES) $@

$(NATIONAL_DATASET_ENTRIES): bin/entries.py $(TRANSFORMED_FILES) $(SCHEMA) index/resource-organisation.csv
	@mkdir -p $(INDEX_DIR)
	python3 bin/entries.py $(TRANSFORMED_DIR) $@

$(COLLECTION_INDEX): bin/index.py $(LOG_FILES) $(VALIDATION_FILES)
	@mkdir -p $(INDEX_DIR)
	python3 bin/index.py $(DATASET_NAME)

$(COLLECTION_INDEXES): $(COLLECTION_INDEX)

#
#  pipeline indexes
#
$(INDEX_DIR)fixed.csv: bin/fixed.py $(FIXED_FILES)
	@mkdir -p $(INDEX_DIR)
	python3 bin/fixed.py $@

$(INDEX_DIR)column.csv: bin/columns.py $(NORMALISED_FILES)
	@mkdir -p $(INDEX_DIR)
	python3 bin/columns.py $@

$(INDEX_DIR)issue.csv: bin/issue.py $(ISSUE_FILES)
	@mkdir -p $(INDEX_DIR)
	python3 bin/issue.py $(ISSUE_DIR) $@

#
#  counts
#
$(COUNT_DIR)column.csv: bin/columns.py $(NORMALISED_FILES)
	@mkdir -p $(COUNT_DIR)
	python3 bin/columns.py $@

$(COUNT_DIR)%.csv: $(MAPPED_DATASET) bin/count.sh
	@mkdir -p $(COUNT_DIR)
	bin/count.sh `basename $@ .csv` < $(MAPPED_DATASET) > $@

$(MAPPED_DATASET): $(MAPPED_FILES) bin/csvcat.sh bin/csvescape.py
	mkdir -p $(TMP_DIR)
	bin/csvcat.sh $(MAPPED_FILES) | bin/csvescape.py > $@

#
#  validation
#
#  -- depends on the schema, but this is expensive to rebuild during development
#
$(VALIDATION_DIR)%.json: $(RESOURCE_DIR)%
	@mkdir -p $(VALIDATION_DIR)
	validate --exclude-input --exclude-rows --file $< --output $@
	@rm -f $<.csv

# fix validation which the validator fails on ..
$(BROKEN_VALIDATIONS):
	@mkdir -p $(VALIDATION_DIR)
	echo '{ "meta_data": {}, "result": {"tables":[{}]} }' > $@

#
#  pipeline to build national dataset
#
$(CONVERTED_DIR)%.csv: $(RESOURCE_DIR)% bin/convert.py
	@mkdir -p $(CONVERTED_DIR)
	python3 bin/convert.py $< $@

$(NORMALISED_DIR)%.csv: $(CONVERTED_DIR)%.csv bin/normalise.py $(NORMALISE_DATA)
	@mkdir -p $(NORMALISED_DIR)
	python3 bin/normalise.py $< $@

$(MAPPED_DIR)%.csv: $(NORMALISED_DIR)%.csv bin/map.py $(SCHEMA)
	@mkdir -p $(MAPPED_DIR)
	python3 bin/map.py $< $@ $(SCHEMA)

$(HARMONISED_DIR)%.csv: $(MAPPED_DIR)%.csv bin/harmonise.py $(SCHEMA) $(HARMONISE_DATA)
	@mkdir -p $(HARMONISED_DIR) $(ISSUE_DIR)
	python3 bin/harmonise.py $< $@ $(SCHEMA) $(subst $(HARMONISED_DIR),$(ISSUE_DIR),$@)

$(TRANSFORMED_DIR)%.csv: $(HARMONISED_DIR)%.csv bin/transform.py $(SCHEMA)
	@mkdir -p $(TRANSFORMED_DIR)
	python3 bin/transform.py $< $@ $(SCHEMA)

$(FIXED_CONVERTED_FILES):
	@mkdir -p $(CONVERTED_DIR)
	python3 bin/convert.py $(subst $(CONVERTED_DIR),$(FIXED_DIR),$@) $@

# local copies of registers
$(CACHE_DIR)/organisation.csv:
	@mkdir -p $(CACHE_DIR)
	curl -qs "https://raw.githubusercontent.com/digital-land/organisation-dataset/master/collection/organisation.csv" > $@

black:
	black .

clobber-today::
	rm -rf $(LOG_FILES_TODAY)

clear-cache:
	rm -rf $(CACHE_DIR)

init::
	pip3 install --upgrade -r requirements.txt

prune:
	rm -rf ./var $(VALIDATION_DIR)
