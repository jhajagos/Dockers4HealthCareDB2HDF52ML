#!/bin/bash

python /root/Git/TransformDBtoHDF5ML/scripts/build_hdf5_matrix_from_document.py -a ohdsi_mapped \
 -b /root/ohdsi/build_hdf5/mapped_ohdsi_cdm_batches.json \
 -c /root/Git/MappingOHDSI2HDF5/mappings/5.2/ohdsi_json_2_hdf5.json \
    /root/Git/MappingOHDSI2HDF5/mappings/5.2/ohdsi_measurement_values_json_2_hdf5.json \
    /root/Git/MappingOHDSI2HDF5/mappings/5.2/ohdsi_observation_values_json_2_hdf5.json \
    /root/Git/MappingOHDSI2HDF5/mappings/5.2/ohdsi_source_codes_json_2_hdf5.json