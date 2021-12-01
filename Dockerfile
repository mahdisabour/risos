FROM python:3.8.5-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
# ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 


# copy requirement to image
COPY ./requirements.txt $APP_HOME

# select working directory
WORKDIR $APP_HOME

# install dependencies
# update packages
RUN apt-get update

# install dependenceis for postgis database
# you should add psycopg2-binary in requirement.txt  
RUN apt-get -y install binutils libproj-dev gdal-bin gdal-bin libgdal-dev python3-gdal postgis
# update pip 
RUN pip install --upgrade pip

# install requirement for django app
RUN apt-get update \
    && pip install -r requirements.txt 
# copy app file to working directory 
COPY . $APP_HOME