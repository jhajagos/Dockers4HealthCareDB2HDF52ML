FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y vim

# Get Python 3.6 source
RUN cd ~/; mkdir src; cd src; wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz ; tar -xzf Python-3.6.5.tgz

RUN cd ~/src/Python-3.6.5/; ./configure --enable-optimizations; make altinstall

RUN apt-get install -y libpq-dev

RUN pip3.6 install --upgrade pip
RUN pip3.6 install sqlalchemy
RUN pip3.6 install ipython
RUN pip3.6 install psycopg2

RUN apt-get install -y default-jre
RUN apt-get install -y unzip

# More commands to setup DockerFile for mapping sources
RUN mkdir ~/Git; cd ~/Git; git clone https://github.com/jhajagos/CommonDataModelMapper.git
RUN mkdir ~/ohdsi/; mkdir ~/ohdsi/vocabulary

RUN mkdir ~/ohdsi/input
RUN mkdir ~/ohdsi/output

COPY ./vocabulary/vocabulary_download_v5.zip /root/ohdsi/vocabulary

RUN mkdir ~/ohdsi/scripts/