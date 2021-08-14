FROM python:3.8.5-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
# RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
# ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt $APP_HOME

WORKDIR $APP_HOME

# install dependencies
RUN apt-get update 
RUN apt-get -y install binutils libproj-dev gdal-bin gdal-bin libgdal-dev python3-gdal postgis
RUN pip install --upgrade pip
RUN apt-get update \
    && pip install -r requirements.txt 
COPY . $APP_HOME

# RUN chown -R app:app $APP_HOME
# RUN chmod 755 $APP_HOME
# USER app