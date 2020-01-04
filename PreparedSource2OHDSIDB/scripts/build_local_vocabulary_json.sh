#!/bin/bash

# The assumption is that the vocabulary file has been named
#

# Unzip vocabulary
cd /root/ohdsi/vocabulary

rm *.csv *.bat readme.txt *.jar *.sh
unzip ohdsi_vocab.zip

# Run java file to extract out CPT codes
# Please edit this file in a running docker or set environment variables and put your UMLS credentials here: https://uts.nlm.nih.gov/home.html
java  -Dumls-user=$UMLS_USER_NAME -Dumls-password=$UMLS_PASSWORD --add-modules=java.xml.ws -jar cpt4.jar 5

# Build JSON
cd ~/ohdsi
python3 ~/Git/CommonDataModelMapper/omop_cdm/utility_programs/generate_code_lookup_json.py -c ~/ohdsi/config/ps_2_cdm_config.json