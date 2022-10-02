FROM python:3.10.4
RUN apt-get update && apt-get -y install cron

COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

RUN mkdir /scripts
