FROM nginx:1.19-alpine

RUN apk add --no-cache certbot

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/neupic_api.conf /etc/nginx/conf.d/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "../entrypoint.sh" ]