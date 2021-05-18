FROM python:3.9.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apk add --update --no-cache postgresql-client

RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev jpeg-dev zlib-dev

RUN pip install -r ./requirements.txt

RUN apk del .tmp-build-deps
