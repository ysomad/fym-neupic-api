FROM nginx:1.19-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/neupic_api.conf /etc/nginx/conf.d/
