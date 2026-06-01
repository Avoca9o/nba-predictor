#!/bin/bash
# Start MLflow server (run from virtual environment)

pip3 install mlflow
mkdir mlruns_local
mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns_local
