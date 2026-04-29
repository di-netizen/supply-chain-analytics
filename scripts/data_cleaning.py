import pandas as pd
import numpy as np
import os

# ---------------- SETUP ---------------- #
np.random.seed(42)
n = 1000

# Ensure folders exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ---------------- DATA GENERATION ---------------- #
data = pd.DataFrame({
    "shipment_id": range(1, n+1),
    "order_id": np.random.randint(1000, 2000, n),
    "origin": np.random.choice(["Mumbai", "Delhi", "Bangalore"], n),
    "destination": np.random.choice(["Pune", "Chennai", "Hyderabad"], n),
    "distance_km": np.random.randint(50, 2000, n),
    "shipment_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 30, n), unit="D"),
})

data["delivery_date"] = data["shipment_date"] + pd.to_timedelta(np.random.randint(1, 10, n), unit="D")

data["delivery_status"] = np.where(
    (data["delivery_date"] - data["shipment_date"]).dt.days > 5,
    "Delayed",
    "On-Time"
)

data["transport_cost"] = data["distance_km"] * np.random.uniform(5, 15, n)

data["vehicle_type"] = np.random.choice(["Truck", "Van", "Bike"], n)

# Save raw data
data.to_csv("data/raw/shipments.csv", index=False)

print("Raw data created!")

# ---------------- CLEANING ---------------- #

# Remove duplicates
data = data.drop_duplicates()

# Handle missing values
data = data.fillna({
    "transport_cost": data["transport_cost"].mean(),
    "vehicle_type": "Unknown"
})

# Ensure correct datatypes
data["shipment_date"] = pd.to_datetime(data["shipment_date"])
data["delivery_date"] = pd.to_datetime(data["delivery_date"])

# Create delivery time column
data["delivery_time_days"] = (data["delivery_date"] - data["shipment_date"]).dt.days

# Remove unrealistic values
data = data[data["distance_km"] > 0]
data = data[data["transport_cost"] > 0]

# Save cleaned data
data.to_csv("data/processed/shipments_cleaned.csv", index=False)

print("Cleaned data saved!")

# Debug path
print("Current working directory:", os.getcwd())