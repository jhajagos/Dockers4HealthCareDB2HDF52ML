"""
python3 ~/Git/CommonDataModelMapper/omop_cdm/utility_programs/generate_concept_load_psql.py -s rw_covid_ohdsi_202011 -c /root/ohdsi/vocabulary/ -f psql_load_concept_tables.sql

psql -U ohdsi -h bmi-rw-translator-2 -p 5433 ohdsi < psql_load_concept_tables.sql

python3 ~/Git/CommonDataModelMapper/omop_cdm/utility_programs/build_files_for_bulk_loading_into_db.py -c ../config/ps_2_cdm_config.json

python3 ~/Git/CommonDataModelMapper/omop_cdm/utility_programs/build_files_for_bulk_loading_into_db.py -c ../config/ps_2_cdm_config.json

cd ../output/

psql -U ohdsi -h bmi-rw-translator-2 -p 5433 ohdsi < load_psql_cdm_tables.sql

"""