QueueLK – ML Prediction Service

Overview 📌

QueueLK ML Prediction Service is a machine learning microservice designed to estimate queue waiting times. It integrates with the QueueLK mobile application (built in Flutter and connected to Firestore) by providing predictions through a Flask API endpoint.

Features 🚀

Random Forest model trained on queue data

Flask API endpoint (/predict) for predictions

Accepts JSON input with arrival time, start time, and queue length

Returns estimated wait time in minutes

Designed to integrate seamlessly with mobile apps

Installation ⚙️

Clone the repository:

git clone https://github.com/YourUsername/QueueLK-ML-Service.git
cd QueueLK-ML-Service

Install dependencies:

python -m pip install -r requirements.txt

Usage 🖥️

Run the Flask API:

python app.py

The API will start locally at http://127.0.0.1:5000.

Example Request 📡

POST request to /predict:

{
  "arrival_minutes": 600,
  "start_minutes": 610,
  "queue_length": 25
}

Example Response 📩

{
  "EstimatedWaitTime": 12.34
}

Project Structure 📂

app.py → Flask API service

models/queue_model.pkl → Trained Random Forest model

scripts/ → Data preprocessing and training scripts

requirements.txt → Dependencies

.gitignore → Ignore sensitive files (e.g., Firebase config)

Contributing 🤝

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License 📄

This project is licensed under the MIT License.
