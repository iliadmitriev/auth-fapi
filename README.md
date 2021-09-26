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
