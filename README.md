# Dockers and scripts for mapping data to OHDSI and to HDF5 file formats for machine learning

## Build docker images

### Upload Athena generated vocabulary to S3

Due to copyright issues with medical vocabularies the process of vocabulary building requires manual intervention. For the
automated docker build process we need to upload the vocabulary to an S3 bucket. The s3 bucket is based on unique hash for
the zip file.

http://athena.ohdsi.org/vocabulary/list

Select the vocabularies that you want to to include. For most modern 
EHR systems you will want: SNOMED, CPT4, HCPCS,
LOINC, RxNorm, NDC, Gender, Race, CMS Place of Service, ATC, Revenue Codes, 
Ethnicity, NUCC, SPL, ICD10CM, ICDCM, and ICD9Proc.

```bash
python upload_vocabulary_to_s3.py
```

This will generate a URL which will be used by the Docker container to build
the needed mappings for OHDSI.

You will need to copy or deploy "s3.ohdsi_vocab.download.txt" into the Docker 
container.

### Upload RxNorm to S3 

Optional for mapping additional drug vocabularies to RxNorm such as Multum.

```bash
python upload_rxnorm_to_s3.py
```

### Build vocabulary file within a Docker Container

A separate container is run to build the vocabulary mapping files. This should only
need to be done once with each vocabulary release. By mounting an external volume
it can be used by other. You will need a UMLS account and
username. This is needed to add CPT codes to the concept vocabulary.

```bash
# On the host
cd /data/
mkdir /data/ohdsi/vocabulary/20190906/ # Directory to build vocabulary into
```

```bash
cd ~/git/Dockers4HealthCareDB2HDF52ML/PreparedSource2OHDSIDB/
docker build --no-cache -t ps2ohdsi:latest ./
docker run -e  UMLS_PASSWORD=password -e UMLS_USER_NAME=username -v /data/ohdsi/vocabulary/20190906/:/root/ohdsi/vocabulary/--name ohdsi_vocabluary ps2ohdsi:latest
```

```bash
docker exec -it ohdsi_vocabulary /bin/bash
cd /root/ohdsi/scripts/
bash build_vocabulary_json.sh
```

### Map Health Facts data to prepared_source format CSV files

As an example data from Health Facts will be mapped to a prepared source
format.

### Map prepared source to OHDSI CSV files

In general you want to start with data in the prepared source format. Details on
the format is here: 
https://github.com/jhajagos/CommonDataModelMapper/tree/master/omop_cdm/
It is an intermediary format for mapping data into OHDSI.

```bash
cd /root/ohdsi/scripts/
bash map_hf_to_prepared_sources.sh
```

### Load OHDSI CSV files into a PostGreSQL database

If you don't have a PostGreSQL database deployed you can use a Docker.
```bash
docker run -p postgres:latest
```

You will need to edit the `ps_2_cdm_config.json` for the connection string
and database schema settings.

```bash
cd /root/ohdsi/config/
vim ps_2_cdm_config.json
```

```json
{
   "json_map_directory": "/root/ohdsi/vocabulary/",
   "csv_input_directory":  "/root/ohdsi/input/",
   "csv_output_directory": "/root/ohdsi/output/",
   "connection_uri": "postgresql+psycopg2://postgres@host.docker.internal:32768/postgres",
   "schema": "ohdsi_cdm",
   "rxnorm_base_directory": "/root/ohdsi/rxnorm/rrf/"
}
```

### Generate HDF5 files in a Docker Container

A single command within the container will run the pipeline. This command will
generate the map2 tables in the PostGreSQL database, compressed JSON.gz files, and the 
final HDF5 files.
```bash
cd /root/ohdsi/scripts/
./run_pipeline.sh
```

