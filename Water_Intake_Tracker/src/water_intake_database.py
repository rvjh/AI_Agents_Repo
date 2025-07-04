import sqlite3
from datetime import datetime
import os

DB_NAME = 'water_tracker.db'

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS water_intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            intake_ml INTEGER,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database and table ready at: {os.path.abspath(DB_NAME)}")  # Debug line

def log_intake(user_id, intake_ml):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date_today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        INSERT INTO water_intake (user_id, intake_ml, date) 
        VALUES (?, ?, ?)
    ''', (user_id, intake_ml, date_today))
    conn.commit()
    conn.close()

def get_intake_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT intake_ml, date 
        FROM water_intake 
        WHERE user_id = ?
    ''', (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

# Create the DB and table
create_tables()

# # Log a test intake to ensure it works
# log_intake('test_user', 500)

# # Fetch and print intake history
# history = get_intake_history('test_user')
# print("Water intake history for test_user:", history)
