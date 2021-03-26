from flask import Flask, jsonify
app = Flask(__name__)

VERSION = "dev-0.0.15"

@app.route("/healthz", methods=["GET"])
def healthz():
    return jsonify(
            statusCode=200,
            version=VERSION,
            status="OK"
        )


@app.route("/ml/audit", methods=["POST"])
def ml_audit():
    return jsonify(
            statusCode=200,
            version=VERSION,
            model="ML"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0")
