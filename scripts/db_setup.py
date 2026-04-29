import pandas as pd
import sqlite3
import os

# ---------------- PATH CHECK ---------------- #
file_path = "data/processed/shipments_cleaned.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found. Run data_cleaning.py first.")

# ---------------- LOAD DATA ---------------- #
df = pd.read_csv(file_path)

# ---------------- CREATE DATABASE ---------------- #
conn = sqlite3.connect("data/logistics.db")

df.to_sql("shipments", conn, if_exists="replace", index=False)

print("Database created successfully!")

# ---------------- VERIFY ---------------- #
result = pd.read_sql("SELECT * FROM shipments LIMIT 5", conn)
print(result)

conn.close()