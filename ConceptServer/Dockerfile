FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y dos2unix

# Get Python 3.6 source
RUN cd ~/; mkdir src; cd src; wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz ; tar -xzf Python-3.6.5.tgz

RUN cd ~/src/Python-3.6.5/; ./configure --enable-optimizations; make altinstall

RUN pip3.6 install --upgrade pip
RUN pip3.6 install sqlalchemy
RUN pip3.6 install ipython
RUN pip3.6 install flask

# More commands to setup DockerFile for mapping sources
RUN mkdir ~/Git; cd ~/Git; git clone https://github.com/jhajagos/CommonDataModelMapper.git
RUN mkdir ~/ohdsi/; mkdir ~/ohdsi/vocabulary
RUN mkdir ~/ohdsi/vocabulary/db/
COPY db/ohdsi_concept.db3 /root/ohdsi/vocabulary/db/
COPY config/config.json /root/Git/CommonDataModelMapper/omop_cdm/concept_server/

RUN mkdir ~/scripts/
COPY scripts/run_concept_server.sh /root/scripts

RUN dos2unix /root/scripts/*
RUN chmod u+x /root/scripts/*

ENTRYPOINT ["/root/scripts/run_concept_server.sh"]