```sh
docker build . --tag airflow_extended:latest
docker run --name scripts-development --rm -itd --mount type=bind,source="$(pwd)",target=/scripts --env-file .env script-dev
```
