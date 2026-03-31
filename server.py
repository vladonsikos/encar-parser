from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import json

app = Flask(__name__, static_folder="static")
CORS(app)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/cars")
def cars():
    try:
        with open("cars.json", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "No data yet. Run encar_parser.py first."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
