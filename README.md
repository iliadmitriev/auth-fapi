# Auth microservice

This program is for educational purposes. It's created using FastAPI and pydantic.

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
pip install fastapi uvicorn\[standard\]
```

4. Create database
* create `.env` file for docker
```shell
cat > .env << _EOF_
POSTGRES_HOST=192.168.10.1
POSTGRES_PORT=5432
POSTGRES_DB=auth
POSTGRES_USER=auth
POSTGRES_PASSWORD=authsecret
_EOF_

export $(cat .env | xargs)
```
* create postgres container with docker
```shell
docker run -d --name auth-fapi-postgres --hostname auth-fapi-postgres \
    -p 5432:5432 --env-file .env postgres:13.4-alpine3.14
```
* run migrations
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
```shell
docker run -d -p 8000:8000 --name auth-fapi --hostname auth-fapi auth-fapi:latest 
```

# Usage

## API documentation

1. Swagger Documentation http://127.0.0.1:8000/docs
2. ReDoc http://127.0.0.1:8000/redoc