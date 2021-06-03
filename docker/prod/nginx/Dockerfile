FROM nginx:1.2-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/neupic_api.conf /etc/nginx/conf.d/
