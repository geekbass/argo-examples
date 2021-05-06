# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier,
# 47(4):547-553, 2009.

"""
This file was forked from MLFlows Examples:
https://github.com/mlflow/mlflow/blob/master/examples/sklearn_elasticnet_wine/train.py
"""

import os
import warnings
import sys

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

# Set the Remote Tracking Server Information
mlflow.set_tracking_uri("http://mlflow")
os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://minio"
os.environ['AWS_ACCESS_KEY_ID'] = "minio"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio123"

# Get the Experiment ID to pass to the run and create it if it doesnt exist
experiment = mlflow.get_experiment_by_name(os.getenv("EXPERIMENT_NAME"))
if experiment is None:
    mlflow.create_experiment(os.getenv("EXPERIMENT_NAME"))

experiment_id = mlflow.get_experiment_by_name(os.getenv("EXPERIMENT_NAME")).experiment_id



def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # Read the wine-quality csv file from the URL
    csv_url = os.getenv("CSV_URL")
    try:
        data = pd.read_csv(csv_url, sep=";")
    except Exception as e:
        logger.exception(
            "Unable to download training & test CSV, check your internet connection. Error: %s", e
        )

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.9
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run(experiment_id=experiment_id):
        # Create the Model
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        model.fit(train_x, train_y)

        predicted_qualities = model.predict(test_x)

        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        # Log the metrics
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        # Log the CSV
        mlflow.log_artifact(local_path='wine_data.csv')
        # Log the train.py
        mlflow.log_artifact(local_path='train.py')
        # Register the model. It will overwrite to a new version if filename exists.
        # This will register as the name of the below name but will be an artifact called model.pkl
        mlflow.sklearn.log_model(sk_model=model,
                                 artifact_path='wine-model',
                                 registered_model_name='wine-model')
