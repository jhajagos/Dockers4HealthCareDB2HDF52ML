FROM ubuntu:latest

RUN apt-get update -y

RUN ln -fs /usr/share/zoneinfo/US/Eastern /etc/localtime #&& dpkg-reconfigure -f noninteractive tzdata

RUN apt-get install -y build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev  libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

RUN apt-get install -y git
RUN apt-get install -y wget
RUN apt-get install -y vim

# Get Python 3.6 source
RUN cd ~/; mkdir src; cd src; wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz ; tar -xzf Python-3.6.5.tgz
RUN cd ~/src/Python-3.6.5/; ./configure --enable-optimizations; make altinstall
RUN pip3.6 install --upgrade pip

RUN pip3.6 install h5py
RUN pip3.6 install numpy
RUN pip3.6 install scipy
RUN pip3.6 install matplotlib
RUN pip3.6 install seaborn
RUN pip3.6 install -U scikit-learn
RUN pip3.6 install jupyter

# Create a new system user
RUN useradd -ms /bin/bash ml

# Change to this new user
USER ml

# Set the container working directory to the user home folder
WORKDIR /home/ml

RUN mkdir /home/ml/notebooks
COPY notebooks/* /home/ml/notebooks

RUN mkdir /home/ml/data

# Start the jupyter notebook
ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0"]

EXPOSE 8888
EXPOSE 9000