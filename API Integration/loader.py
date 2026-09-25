import requests
import psycopg2

# Step 1: Extract - call the API
resp = requests.get("https://jsonplaceholder.typicode.com/users")
resp.raise_for_status()
users = resp.json()
print(f"Fetched {len(users)} users from API")

# Step 2: Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="mydb",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Step 3: Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    city TEXT
)
""")

# Step 4: Load - insert data
for u in users:
    cur.execute(
        """INSERT INTO customers (customer_id, name, username, email, city)
           VALUES (%s, %s, %s, %s, %s)
           ON CONFLICT (customer_id) DO NOTHING""",
        (u["id"], u["name"], u["username"], u["email"], u["address"]["city"])
    )

conn.commit()
print("Data loaded into PostgreSQL successfully")

cur.close()
conn.close()