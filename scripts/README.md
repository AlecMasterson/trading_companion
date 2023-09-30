# Setup

Utilize Docker to setup the backend API and an environment for running scripts.

## Docker Build

```shell
cd scripts
docker build . --tag scripts:1.0.0`
```

## Docker Compose

`docker compose run --rm -itd -p 8000:8000 scripts`
