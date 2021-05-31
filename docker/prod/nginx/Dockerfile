FROM jwilder/nginx-proxy

COPY ./docker/prod/nginx/vhost.d/default /etc/nginx/vhost.d/default
RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/neupic_api.conf /etc/nginx/conf.d/
