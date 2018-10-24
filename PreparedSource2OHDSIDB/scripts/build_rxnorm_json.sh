#!/bin/bash

cd /root/ohdsi/rxnorm/
wget $(cat s3.rxnorm.download.txt)

unzip rxnorm_full.zip

python3.6 /root/Git/CommonDataModelMapper/omop_cdm/utility_programs/rxnorm/rxnorm_sourced_multum_mappings.py -c /root/ohdsi/config/ps_2_cdm_config.json