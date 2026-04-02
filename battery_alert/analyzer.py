import sqlite3
import re
import pandas as pd

DB_PATH = "data/battery.db"

def get_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM battery_logs", conn)
    conn.close()
    return df


def estimate_drain_rate():
    df = get_data()

    if len(df) < 5:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["percent"] = df["percent"].astype(int)

    df = df.tail(5)

    time_diff = (df["timestamp"].iloc[-1] - df["timestamp"].iloc[0]).total_seconds() / 60
    percent_diff = df["percent"].iloc[0] - df["percent"].iloc[-1]

    if time_diff <= 0:
        return None

    return percent_diff / time_diff


def estimate_time_remaining(current_percent):
    rate = estimate_drain_rate()

    if rate is None or rate <= 0:
        return None

    return round(current_percent / rate, 2)

def get_real_battery_health():
    try:
        with open("battery_report.html", "r", encoding="utf-8") as f:
            content = f.read()

        design = re.search(r"DESIGN CAPACITY.*?(\d+)", content)
        full = re.search(r"FULL CHARGE CAPACITY.*?(\d+)", content)

        if design and full:
            design_val = int(design.group(1))
            full_val = int(full.group(1))

            health = (full_val / design_val) * 100
            return int(health)

    except Exception as e:
        print("Health read error:", e)

    return None