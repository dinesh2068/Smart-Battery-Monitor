import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "data/battery.db"

def show_graph():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM battery_logs", conn)
    conn.close()

    if df.empty:
        print("No data")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    plt.figure()
    plt.plot(df["timestamp"], df["percent"])
    plt.xlabel("Time")
    plt.ylabel("Battery %")
    plt.title("Battery Usage Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()