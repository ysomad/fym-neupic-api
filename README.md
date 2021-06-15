# fym-neupic-queue

## Development
1. Build docker image
```bash
$ docker-compose build
```
2. Run docker containers
```bash
$ docker-compose up -d
```

## Production
1. Create and fill in `.env.prod` with db credentials
2. Build production docker compose
```bash
$ docker-compose -f docker-compose.prod.yml build
```
3. Run docker containers
```bash
$ docker-compose -f docker-compose.prod.yml up -d
```
4. Create super user, collectstatic and makemigrations for JWT tokens
Connect to django container
```bash
$ docker exec -ti django sh
$ /usr/src/app/: python manage.py collectstatic
$ /usr/src/app/: python manage.py createsuperuser
$ /usr/src/app/: python manage.py makemigrations
$ /usr/src/app/: python manage.py migrate
```
