cd /root/Git/MappingOHDSI2HDF5/sql/
python execute_sql_files.py -f ./5.3/create_denormalized_tables_5_3.sql -c "postgresql+psycopg2://postgres@172.17.0.7:5432/postgres" -s ohdsi_cdm