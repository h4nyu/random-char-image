FROM python:3.8-slim

WORKDIR /srv
COPY . .
RUN pip install -e .[dev]
