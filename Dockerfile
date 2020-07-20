# Dockerfile
# Pull base image
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
COPY . ./code/
WORKDIR /code

RUN pip install pipenv
RUN pipenv install
