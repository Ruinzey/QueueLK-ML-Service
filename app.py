from flask import Flask, request, jsonify
import joblib
import numpy as np
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = joblib.load("models/queue_model.pkl")

def time_to_minutes(dt: datetime) -> int:
    """Convert datetime to minutes of day"""
    return dt.hour * 60 + dt.minute

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status":  "QueueLK AI API Running",
        "version": "1.0.0",
        "endpoints": ["/predict", "/predict-now"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict wait time from provided values.
    Body: {
        "arrival_minutes": 600,
        "start_minutes": 610,
        "queue_length": 25
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        arrival_minutes = data.get('arrival_minutes', 0)
        start_minutes   = data.get('start_minutes', 0)
        queue_length    = data.get('queue_length', 0)

        features = np.array([[
            arrival_minutes,
            start_minutes,
            queue_length
        ]])

        prediction = model.predict(features)[0]

        # Ensure prediction is positive
        predicted_wait = max(1, round(float(prediction), 2))

        return jsonify({
            "EstimatedWaitTime": predicted_wait,
            "unit":              "minutes",
            "queue_length":      queue_length,
            "status":            "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/predict-now', methods=['POST'])
def predict_now():
    """
    Predict wait time using current time automatically.
    Body: {
        "queue_length": 25
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        queue_length = data.get('queue_length', 0)

        # Use current time for arrival and start
        now             = datetime.now()
        arrival_minutes = time_to_minutes(now)
        start_minutes   = arrival_minutes + 2

        features = np.array([[
            arrival_minutes,
            start_minutes,
            queue_length
        ]])

        prediction = model.predict(features)[0]

        predicted_wait = max(1, round(float(prediction), 2))

        return jsonify({
            "EstimatedWaitTime": predicted_wait,
            "unit":              "minutes",
            "queue_length":      queue_length,
            "arrival_minutes":   arrival_minutes,
            "start_minutes":     start_minutes,
            "status":            "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Allow connections from all devices on local network
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
    