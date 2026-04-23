from flask import Flask, request, jsonify
import joblib
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = joblib.load("models/queue_model.pkl")

# Initialize Firebase
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_latest_queue_length():
    # Fetch latest queue_length from Firestore
    docs = db.collection("queues").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1).stream()
    for doc in docs:
        return doc.to_dict().get("queue_length", 0)
    return 0

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    features = np.array([[data['arrival_minutes'],
                          data['start_minutes'],
                          data['queue_length']]])

    prediction = model.predict(features)[0]
    return jsonify({"EstimatedWaitTime": round(prediction, 2)})


if __name__ == "__main__":
    app.run(debug=True)
