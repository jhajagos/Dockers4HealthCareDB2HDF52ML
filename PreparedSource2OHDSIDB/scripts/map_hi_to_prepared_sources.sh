#!/bin/bash

python3.6 /root/Git/CommonDataModelMapper/omop_cdm/hi_etl_to_prepared_source.py -c /root/ohdsi/config/ps_2_cdm_config.json

python3.6 /root/Git/CommonDataModelMapper/omop_cdm/transform_prepared_source_to_cdm.py -c /root/ohdsi/config/ps_2_cdm_config.json