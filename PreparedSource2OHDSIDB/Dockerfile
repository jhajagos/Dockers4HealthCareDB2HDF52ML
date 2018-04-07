FROM ubuntu:latest

RUN apt-get update -y

RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN apt-get install -y git
RUN apt-get install -y wget


RUN cd ~/; mkdir src; cd src; wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz ; tar -xzf Python-3.6.5.tgz

RUN cd ~/src/Python-3.6.5/; ./configure --enable-optimizations; make altinstall

# More commands to setup DockerFile for mapping sources