import pandas as pd
import numpy as np

# Load dataset
data = pd.read_csv("data/queue_data.csv")

# Convert arrival_time and start_time into numeric minutes of day
def convert_time(t):
    try:
        hh_mm = t.split(" ")[1]   # take the HH.MM part
        hh, mm = hh_mm.split(".")
        return int(hh) * 60 + int(mm)
    except:
        return np.nan

data["arrival_minutes"] = data["arrival_time"].apply(convert_time)
data["start_minutes"] = data["start_time"].apply(convert_time)

# Drop rows with missing values
data = data.dropna()

# Save the processed dataset for training
data.to_csv("data/processed_queue_data.csv", index=False)

print("✅ Preprocessing complete. Saved to data/processed_queue_data.csv")
