#!/bin/bash

python3 /root/Git/CommonDataModelMapper/omop_cdm/utility_programs/load_schema_into_db.py -c /root/ohdsi/config/ps_2_cdm_config.json  --ddl-file ~/Git/CommonDataModelMapper/omop_cdm/schema/5.3/omop_cdm.sql  --schema-customization-file ~/Git/CommonDataModelMapper/omop_cdm/schema/5.3/alter_schema.sql

python3 /root/Git/CommonDataModelMapper/omop_cdm/utility_programs/load_concept_files_into_db.py -c ~/ohdsi/config/ps_2_cdm_config.json

python3 /root/Git/CommonDataModelMapper/omop_cdm/utility_programs/load_mapped_cdm_files_into_db.py -c /root/ohdsi/config/ps_2_cdm_config.json