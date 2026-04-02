import sqlite3

DB_PATH = "data/battery.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS battery_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        percent INTEGER,
        plugged INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_data(data):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO battery_logs (timestamp, percent, plugged)
    VALUES (?, ?, ?)
    """, (data["timestamp"], data["percent"], data["plugged"]))

    conn.commit()
    conn.close()