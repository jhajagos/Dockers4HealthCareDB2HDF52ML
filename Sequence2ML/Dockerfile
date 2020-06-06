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
RUN pip3 install h5py

RUN apt-get install -y unzip

# More commands to setup DockerFile for mapping sources
RUN mkdir ~/Git; cd ~/Git; git clone https://github.com/jhajagos/TimeWeaver.git
RUN cd ~/Git; git clone https://github.com/jhajagos/agile_data_tools.git
RUN cd ~/Git; git clone https://github.com/jhajagos/LSTMSeq2ML.git

RUN mkdir ~/ohdsi/
RUN mkdir ~/ohdsi/input
RUN mkdir ~/ohdsi/output
RUN mkdir ~/ohdsi/output/csv/
RUN mkdir ~/ohdsi/output/hdf5/

RUN mkdir ~/ohdsi/config


RUN mkdir ~/ohdsi/scripts/
# COPY ./scripts/build_vocabulary_json.sh /root/ohdsi/scripts/

RUN apt-get install -y dos2unix
# RUN dos2unix /root/ohdsi/scripts/build_vocabulary_json.sh

# RUN chmod u+x /root/ohdsi/scripts/build_vocabulary_json.sh

COPY ./config/config_export.json /root/ohdsi/config/

COPY ./scripts/generate_export_json.py /root/ohdsi/scripts/

COPY ./scripts/run_sequence_generation.sh /root/ohdsi/scripts/

RUN dos2unix  /root/ohdsi/scripts/run_sequence_generation.sh

RUN chmod u+x  /root/ohdsi/scripts/run_sequence_generation.sh

#COPY ./scripts/bulk_import_data_from_csv_to_db.py /root/ohdsi/scripts/
#COPY ./scripts/generated_csv_input_import.py /root/ohdsi/scripts/
#COPY ./scripts/create_schemas.py /root/ohdsi/scripts/
#
#COPY ./config/prepared_source_template.json /root/ohdsi/config/
