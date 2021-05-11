"""
This file is used to demonstrate how to promote the latest version of a Model to "Production" stage so that it can be
served out of the Model Registry.
"""
import os
import warnings
import sys
from mlflow.tracking import MlflowClient
import mlflow

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Set the Remote Tracking Server Information
tracking_server = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow")
mlflow.set_tracking_uri(tracking_server)
os.environ['MLFLOW_S3_ENDPOINT_URL'] = os.getenv("MLFLOW_ARTIFACT_URI", "http://minio")
os.environ['AWS_ACCESS_KEY_ID'] = "minio"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio123"
# Basic Auth Info
os.environ['MLFLOW_TRACKING_USERNAME'] = "admin"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "password"

# Promote the latest Version of Staging to Production
client = MlflowClient()
model_name = "wine-model"

# Get the latest version of "Staging"
models = client.get_latest_versions(model_name, stages=["None"])
for model in models:
    name = model.name
    latest_version = int(model.version)
    run_id = model.run_id
    current_stage = model.current_stage
    print(name, latest_version)
    # Transition
    client.transition_model_version_stage(
        name=name,
        version=latest_version,
        stage="Production"
    )






