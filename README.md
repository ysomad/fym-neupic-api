# FYM bot tasks manager
API for managing bot tasks

## Short description
In main application users creating tasks which contains function, subfunction and media which needed to be processed.
Bots are located on different independent backends and every bot processing media in different applications which
has different functions and subfunctions. 
1. Just after the task has been created, it's tied to a specific bot that is least loaded
2. Bot takes the task in work, sets it a status 'processing'
3. After processing sets it a status 'done' and uploading processed media and bind it to the task
4. Client downloads processed media from task

## Usage

### Development
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
```bash
$ docker exec -ti django sh
$ /usr/src/app/: python manage.py collectstatic
$ /usr/src/app/: python manage.py createsuperuser
$ /usr/src/app/: python manage.py makemigrations
$ /usr/src/app/: python manage.py migrate
```
