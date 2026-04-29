import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/logistics.db")

# ---------------- QUERY 1 ---------------- #
print("\n--- Delivery Status Count ---")
q1 = """
SELECT delivery_status, COUNT(*) as total
FROM shipments
GROUP BY delivery_status;
"""
df1 = pd.read_sql(q1, conn)
print(df1)

# ---------------- QUERY 2 ---------------- #
print("\n--- Orders per Destination ---")
q2 = """
SELECT destination, COUNT(*) as total
FROM shipments
GROUP BY destination;
"""
df2 = pd.read_sql(q2, conn)
print(df2)

# ---------------- QUERY 3 ---------------- #
print("\n--- Average Delivery Time ---")
q3 = """
SELECT AVG(delivery_time_days) as avg_delivery_time
FROM shipments;
"""
df3 = pd.read_sql(q3, conn)
print(df3)

# ---------------- QUERY 4 ---------------- #
print("\n--- Delay % by Destination ---")
q4 = """
SELECT 
    destination,
    COUNT(*) AS total,
    SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed,
    ROUND(
        100.0 * SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS delay_percentage
FROM shipments
GROUP BY destination
ORDER BY delay_percentage DESC;
"""
df4 = pd.read_sql(q4, conn)
print(df4)

# ---------------- QUERY 5 ---------------- #
print("\n--- Distance vs Delivery Time ---")
q5 = """
SELECT 
    (distance_km/100)*100 AS distance_bucket,
    AVG(delivery_time_days) AS avg_delivery_time
FROM shipments
GROUP BY distance_bucket
ORDER BY distance_bucket;
"""
df5 = pd.read_sql(q5, conn)
print(df5)

# ---------------- QUERY 6 (ADVANCED) ---------------- #
print("\n--- Worst Routes by Delay (Ranking) ---")
q6 = """
SELECT 
    origin,
    destination,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delays,
    RANK() OVER (
        ORDER BY SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) DESC
    ) AS delay_rank
FROM shipments
GROUP BY origin, destination;
"""
df6 = pd.read_sql(q6, conn)
print(df6)

# CLOSE CONNECTION AT END
conn.close()