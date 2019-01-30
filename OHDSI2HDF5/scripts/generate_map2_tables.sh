cd /root/Git/MappingOHDSI2HDF5/sql/
python execute_sql_files.py -f ./5.3/create_denormalized_tables_5_3.sql -c $POSTGRESQL_CONNECTION_STRING -s $SCHEMA_NAME