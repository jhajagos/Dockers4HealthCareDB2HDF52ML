This Dockerfile is for building the tools to map prepared_source format to OHDSI mapped CSV file
which is then loaded into an HDF5 container.

## Build base docker image

```bash
cd ~/git/
git clone https://github.com/jhajagos/Dockers4HealthCareDB2HDF52ML.git
sudo docker build --no-cache ./ -t ps2ohdsi:latest
```

## Build Vocabulary

The first step is to build vocabulary files for mapping. In general you build the 
vocabulary to an externally mounted directory so it can be used for mapping.

```bash
mkdir /data/ohdsi/vocab/51/
# Generated from http://athena.ohdsi.org/
cp "~/vocabulary_download_v5_{204484ab-5169-451d-a163-00d5254866be}_1577376430031.zip" /data/ohdsi/vocab/51/ohdsi_vocab.zip

sudo docker run -v /data/ohdsi/vocab/51/:/root/ohdsi/vocabulary/ --name ohdsivocab -it ps2ohdsi:latest /bin/bash
```
### Within the container 

You will need a UMLS account: https://www.nlm.nih.gov/research/umls/index.html

```bash
# this could be set in docker run
export UMLS_USER_NAME=umlsusername
export UMLS_PASSWORD="YourUMLSPassword"

cd /root/ohdsi/scripts/
bash build_local_vocabulary.sh
```

## Running a docker image for mapping to OHDSI CDM

```bash
sudo docker run -v /data/ohdsi/realworld/covid/20201123/input/:/root/ohdsi/input/ \
    -v /data/ohdsi/realworld/covid/20201123/output/:/root/ohdsi/output/ \
    -v /data/ohdsi/vocabulary/20200517/51m/:/root/ohdsi/vocabulary/ \
    --name rw_covid_ohdsi_202011 \
    -it ps2ohdsi:latest /bin/bash
```

