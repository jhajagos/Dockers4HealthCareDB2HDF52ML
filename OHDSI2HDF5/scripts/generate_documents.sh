#!/bin/bash

python /root/Git/MappingOHDSI2HDF5/sql/execute_sql_files.py -f /root/Git/MappingOHDSI2HDF5/sql/5.3/create_denormalized_tables_5_3.sql -c "postgresql+psycopg2://postgres@host.docker.internal:32768/postgres" -s ohdsi_cdm

python /root/Git/TransformDBtoHDF5ML/scripts/build_document_mapping_from_db.py \
  -c /root/Git/MappingOHDSI2HDF5/mappings/5.3/ohdsi_db_2_json.json -r /root/ohdsi/config/runtime_config.json