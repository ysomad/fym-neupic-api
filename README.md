# FYM bot tasks manager
API for managing bot tasks

## Short description
In main application users creating tasks which contains function, subfunction and media which needed to be processed.
Bots are located on different independent backends and every bot processing media in different applications which
has different functions and subfunctions. 
1. After a task has been created, Celery assigns the newly created task to bot, which is least loaded
2. Bot starts processing media from the task and changes the task status to "processing"
3. After a bot finishes processing, it uploads media to server, sets task status to "done" and attaches processed media to the task
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

### Production
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
