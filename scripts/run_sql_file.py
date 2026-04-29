import sqlite3

# Connect to database
conn = sqlite3.connect("data/logistics.db")
cursor = conn.cursor()

# Read SQL file
with open("sql/queries.sql", "r") as file:
    sql_script = file.read()

# Execute all queries
queries = sql_script.split(";")

for query in queries:
    query = query.strip()
    if query:
        print("\n==============================")
        print("Running Query:")
        print(query)

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Print column names
            columns = [desc[0] for desc in cursor.description]
            print(columns)

            # Print rows
            for row in rows[:10]:  # limit output
                print(row)

        except Exception as e:
            print("Error:", e)

conn.close()