FROM python:3.9.5-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY app/ requirements.txt /usr/src/app/

# install dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev jpeg-dev zlib-dev
RUN pip install --no-cache-dir -r ./requirements.txt
RUN apk del .tmp-build-deps



