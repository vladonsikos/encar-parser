import threading
import schedule
import time
from encar_parser import run
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import json, os

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
        return jsonify({"error": "Data not ready yet, try again in a minute."}), 503


def scheduler_thread():
    schedule.every(24).hours.do(run)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    # Parse on startup if no data
    if not os.path.exists("cars.json"):
        run()

    # Run scheduler in background
    t = threading.Thread(target=scheduler_thread, daemon=True)
    t.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
