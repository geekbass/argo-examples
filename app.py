from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

VERSION = "dev-0.0.16"

# Load the Model
with open('./model.pkl', 'rb') as file:
    model = pickle.load(file)

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
