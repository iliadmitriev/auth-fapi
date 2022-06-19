# Auth microservice

[![CI unittests](https://github.com/iliadmitriev/auth-fapi/actions/workflows/python.yml/badge.svg)](https://github.com/iliadmitriev/auth-fapi/actions/workflows/python.yml)
[![codecov](https://codecov.io/gh/iliadmitriev/auth-fapi/branch/master/graph/badge.svg?token=TNU4TRP8S3)](https://codecov.io/gh/iliadmitriev/auth-fapi)
[![CodeQL](https://github.com/iliadmitriev/auth-fapi/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/iliadmitriev/auth-fapi/actions/workflows/codeql-analysis.yml)

This program is for educational purposes. It's created using FastAPI and pydantic.


- [Auth microservice](#auth-microservice)
- [Install](#install)
- [Tests](#tests)
  * [Install pytest](#install-pytest)
  * [run tests](#run-tests)
  * [install coverage](#install-coverage)
  * [run tests with coverage](#run-tests-with-coverage)
  * [run tests with coverage and check 100%](#run-tests-with-coverage-and-check-100-)
  * [Coverage HTML report](#coverage-html-report)
- [Start Application](#start-application)
  * [Start with hot reload](#start-with-hot-reload)
- [Docker](#docker)
  * [Build image](#build-image)
  * [Run docker container](#run-docker-container)
- [Usage](#usage)
  * [API documentation](#api-documentation)

# Install

1. Create virtual environment
```shell
python3 -m venv venv
```

2. Activate virtual environment
```shell
source venv/bin/activate
```

3. Install pip packages
```shell
pip install -r requirements.txt
```

4. Create database

for postgresql as database

```shell
# setup db, user and password
cat > .env_postgres << _EOF_
POSTGRES_DB=auth
POSTGRES_USER=auth
POSTGRES_PASSWORD=authsecret
_EOF_

# create docker instance of postgresql
docker run -d --name auth-fapi-postgres --hostname auth-fapi-postgres \
    -p 5432:5432 --env-file .env_postgres postgres:14-alpine
```

for mysql as database

```shell
# setup db, user and password
cat > .env_mysql << _EOF
MYSQL_ROOT_PASSWORD=rootsecret
MYSQL_DATABASE=auth
MYSQL_USER=auth
MYSQL_PASSWORD=authsecret
_EOF

# create docker instance of mariadb
docker run -d --name auth-fapi-mariadb --hostname auth-fapi-mariadb \
              --env-file .env_mysql -p 3306:3306 mariadb
```

5. Create redis instance

```shell
docker run -d --name auth-fapi-redis --hostname auth-fapi-redis \
              -p 6379:6379 redis:6.2-alpine
```

6. configure application environment variables

for postgresql

```shell
cat > .env << _EOF_
DATABASE_DRIVER=postgresql+asyncpg
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=auth
DATABASE_USER=auth
DATABASE_PASSWORD=authsecret
_EOF_

export $(cat .env | xargs)
```

for mysql

```shell
cat > .env << _EOF_
DATABASE_DRIVER=mysql+asyncmy
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=auth
DATABASE_USER=auth
DATABASE_PASSWORD=authsecret
_EOF_

export $(cat .env | xargs)
```

add redis url to `.env`

```shell
cat >> .env << _EOF_
REDIS_URL=redis://localhost:6379/0
_EOF_

export $(cat .env | xargs)
```

6. Run migrations

```shell
alembic upgrade head
```

# Tests

Tests located in `tests` directory and based on pytest and using `requests` library

## Install pytest

```shell
pip install pytest requests
```

## run tests

```shell
pytest -v
```

## install coverage

```shell
pip install pytest-coverage
```

## run tests with coverage

```shell
pytest -v --cov=.
```

## run tests with coverage and check 100%

```shell
pytest -v --cov=. --cov-report=term-missing --cov-fail-under=100
```

## Coverage HTML report

```shell
# run tests and generate report
pytest -v --cov=. --cov-report=term-missing --cov-fail-under=100 --cov-report=html

# open report
open htmlcov/index.html 
```

# Start Application

## Start with hot reload

```shell
uvicorn main:app --reload 
```

# Docker

## Build image

```shell
docker build -t auth-fapi ./
```

## Run docker container

setup db environment and run db container

```shell
# setup db, user and password
cat > .env_postgres << _EOF_
POSTGRES_DB=auth
POSTGRES_USER=auth
POSTGRES_PASSWORD=authsecret
_EOF_

# create docker instance of postgresql
docker run -d --name auth-fapi-postgres --hostname auth-fapi-postgres \
    -p 5432:5432 --env-file .env_postgres postgres:13.4-alpine3.14
```

setup environment for application container 

```shell
# setup db, user and password
cat > .env << _EOF_
DATABASE_DRIVER=postgresql+asyncpg
DATABASE_HOST=192.168.10.1
DATABASE_PORT=5432
DATABASE_NAME=auth
DATABASE_USER=auth
DATABASE_PASSWORD=authsecret
_EOF_
```

migrate

```shell
docker run -it --rm --env-file .env auth-fapi:latest \
       alembic upgrade head
```

run application container

```shell
docker run -d -p 8000:8000 --name auth-fapi --hostname auth-fapi \
             --env-file .env auth-fapi:latest
```

# Usage

## API documentation

1. Swagger Documentation http://127.0.0.1:8000/docs
2. ReDoc http://127.0.0.1:8000/redoc
