from flask import Flask, request, jsonify
import pandas as pd
import mlflow.pyfunc
import os

app = Flask(__name__)

VERSION = "dev-0.0.1"

# Set the Remote Tracking Server Information
tracking_server = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow")
mlflow.set_tracking_uri(tracking_server)
os.environ['MLFLOW_S3_ENDPOINT_URL'] = os.getenv("MLFLOW_ARTIFACT_URI", "http://minio")
os.environ['AWS_ACCESS_KEY_ID'] = "minio"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio123"
# Basic Auth Info
os.environ['MLFLOW_TRACKING_USERNAME'] = "admin"
os.environ['MLFLOW_TRACKING_PASSWORD'] = "password"

# Load the Model from MLFlow. By Default MLFlow loads the latest Version.
model_name = "wine-model"
stage = "Production"

model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{model_name}/{stage}"
)

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify(
        statusCode=200,
        version=VERSION,
        status="OK"
    )


@app.route('/predict', methods=['POST'])
def main():
    # Get the request as a JSON
    req = request.get_json()

    # Load the JSON as a DF
    features = pd.DataFrame(req, index=[0])

    # Call the predict method against the model and flatten the nd array to a list type
    quality = model.predict(features).tolist()

    # Return The quality prediction along with 200 code
    return jsonify(
        statusCode=200,
        quality=quality
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
