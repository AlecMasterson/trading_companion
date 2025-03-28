```shell
# to run API for local development
PYTHONPATH=src uvicorn src.api:app --host 0.0.0.0 --port 8080 --reload --reload-dir ./src --reload-exclude '__pycache__/*'
```
