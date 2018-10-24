FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y python
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-dev
RUN apt-get install -y build-essential
RUN apt-get install -y python-pip

RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y vim

RUN pip install --upgrade pip
RUN apt-get install -y libpq-dev

RUN pip install sqlalchemy
RUN pip install sqlparse
RUN pip install ipython
RUN pip install psycopg2
RUN pip install ujson
RUN pip install numpy
RUN pip install h5py

RUN mkdir /root/Git
RUN cd /root/Git; git clone https://github.com/jhajagos/TransformDBtoHDF5ML.git
RUN cd /root/Git; git clone https://github.com/SBU-BMI/MappingOHDSI2HDF5.git

RUN mkdir /root/ohdsi/
RUN mkdir /root/ohdsi/build_hdf5/
RUN mkdir /root/ohdsi/scripts/
RUN mkdir /root/ohdsi/config/

COPY config/runtime_config.json /root/ohdsi/config

RUN apt-get install -y dos2unix