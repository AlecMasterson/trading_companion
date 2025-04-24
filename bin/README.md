```shell
# to run API for local development
PYTHONPATH=src uvicorn src.api:app --host 0.0.0.0 --port 8080 --reload --reload-dir ./src --reload-exclude '__pycache__/*'
# to run Dagster for local development
DAGSTER_HOME=/app PYTHONPATH=/app dagster dev -w dagster_workspace.yaml -h "0.0.0.0" -p 3000
```
