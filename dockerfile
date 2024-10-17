FROM python:3.10-slim

RUN pip install pipenv
WORKDIR /home
COPY Pipfile* ./
RUN pipenv sync -d
