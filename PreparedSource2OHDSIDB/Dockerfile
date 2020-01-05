FROM ubuntu:latest

RUN apt-get update -y
RUN ln -fs /usr/share/zoneinfo/US/Eastern /etc/localtime #&& dpkg-reconfigure -f noninteractive tzdata


RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y less

RUN apt-get install -y libpq-dev

RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y  python3-dev

RUN pip3 install --upgrade pip
RUN pip3 install sqlalchemy
RUN pip3 install ipython
RUN pip3 install psycopg2
RUN pip3 install sqlparse
RUN pip3 install numpy
RUN pip3 install pandas

RUN apt-get -y install software-properties-common
RUN apt-get install -y openjdk-8-jdk

RUN apt-get install -y unzip

# More commands to setup DockerFile for mapping sources
RUN mkdir ~/Git; cd ~/Git; git clone https://github.com/jhajagos/CommonDataModelMapper.git
RUN mkdir ~/ohdsi/; mkdir ~/ohdsi/vocabulary

RUN mkdir ~/ohdsi/input
RUN mkdir ~/ohdsi/output
RUN mkdir ~/ohdsi/config

# Get vocabulary S3
#COPY ./vocabulary/vocabulary_download_v5.zip /root/ohdsi/vocabulary
# As the OHDSI vocabulary is custom generated, once it it is downloaded from Athena, we need to upload to s3
# using upload_vocabulary_to_s3.py which generates the s3.ohdsi_vocab.download.txt which contains the URL to download

COPY ./config/s3.ohdsi_vocab.download.txt /root/ohdsi/config/


RUN mkdir ~/ohdsi/rxnorm/
COPY ./config/s3.rxnorm.download.txt /root/ohdsi/rxnorm/

RUN mkdir ~/ohdsi/scripts/
COPY ./scripts/build_vocabulary_json.sh /root/ohdsi/scripts/
COPY ./scripts/build_local_vocabulary_json.sh /root/ohdsi/scripts/
COPY ./scripts/build_rxnorm_json.sh /root/ohdsi/scripts/
COPY ./scripts/import_ohdsi_database.sh /root/ohdsi/scripts/
COPY ./scripts/map_hf_to_prepared_sources.sh /root/ohdsi/scripts/

RUN apt-get install -y dos2unix
RUN dos2unix /root/ohdsi/scripts/build_vocabulary_json.sh
RUN dos2unix /root/ohdsi/scripts/build_local_vocabulary_json.sh
RUN dos2unix /root/ohdsi/scripts/build_rxnorm_json.sh
RUN dos2unix /root/ohdsi/scripts/import_ohdsi_database.sh
RUN dos2unix /root/ohdsi/scripts/map_hf_to_prepared_sources.sh

RUN chmod u+x /root/ohdsi/scripts/build_vocabulary_json.sh
RUN chmod u+x /root/ohdsi/scripts/build_local_vocabulary_json.sh

COPY ./config/ps_2_cdm_config.json /root/ohdsi/config/

COPY ./scripts/bulk_import_data_from_csv_to_db.py /root/ohdsi/scripts/
COPY ./scripts/generated_csv_input_import.py /root/ohdsi/scripts/
COPY ./scripts/create_schemas.py /root/ohdsi/scripts/

COPY ./config/prepared_source_template.json /root/ohdsi/config/
