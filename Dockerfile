FROM python:3.10-slim

RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y git
RUN  apt-get install -y default-libmysqlclient-dev build-essential