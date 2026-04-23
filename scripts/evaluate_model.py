import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error

data = pd.read_csv("data/processed_queue_data.csv")
X = data[["arrival_minutes", "start_minutes", "queue_length"]]
y = data["wait_time"]

model = joblib.load("models/queue_model.pkl")
preds = model.predict(X)
mae = mean_absolute_error(y, preds)
print("Mean Absolute Error:", mae)
