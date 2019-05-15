FROM python:3.6

RUN pip install pipenv

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y shellcheck \
    && rm -rf /var/lib/apt/lists/*
