FROM python:3.9.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app
WORKDIR /usr/src/app

# install system dependencies

RUN apk add --update --no-cache postgresql-client

# Install individual dependencies
# so that we could avoid installing extra packages to the container
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev curl jpeg-dev zlib-dev

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

RUN poetry config virtualenvs.create false

# Install python dependencies
RUN poetry install --no-dev

RUN apk del .tmp-build-deps

