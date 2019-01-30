#!/bin/bash

python /root/Git/TransformDBtoHDF5ML/scripts/build_document_mapping_from_db.py \
  -c /root/Git/MappingOHDSI2HDF5/mappings/5.3/ohdsi_db_2_json.json -r /root/ohdsi/config/runtime_config.json