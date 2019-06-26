#!/bin/bash

cd ~/ohdsi/scripts/
python3 generate_export_json.py

cd ~/ohdsi/config/
python3 ~/Git/agile_data_tools/bulk_export_from_tables_json.py -j export_tables.json

cd ~/Git/TimeWeaver/src
python3 assemble_sequences.py -j ../ohdsi/config/config_assemble_mapping.json  -i /root/ohdsi/input/ -o /root/ohdsi/output/ohdsi_assembled.json.txt

python3 generate_sequences.py -j ../ohdsi/config/config_sequences.json  -i /root/ohdsi/output/ohdsi_assembled.json.txt -o /root/ohdsi/output/ohdsi_sequence.json.txt

python3 package_sequences.py -f /root/ohdsi/output/ohdsi_sequence.json.txt -c scan -b ohdsi -d /root/ohdsi/output/csv/

python3 package_sequences.py -f /root/ohdsi/output/ohdsi_sequence.json.txt -c csv -b ohdsi -d /root/ohdsi/output/csv/

python3 package_sequences.py -f /root/ohdsi/output/ohdsi_sequence.json.txt -c hdf5 -b ohdsi -d /root/ohdsi/output/csv/