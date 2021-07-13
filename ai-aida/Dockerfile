FROM python:3.8.5-slim-buster


WORKDIR /app


RUN apt-get update
RUN pip install --upgrade pip
RUN apt install -y libprotobuf-dev protobuf-compiler
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

    
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
