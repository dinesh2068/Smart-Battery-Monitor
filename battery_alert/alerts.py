import ctypes
from analyzer import estimate_time_remaining
from config import LOW_BATTERY_THRESHOLD, SMART_ALERT_MINUTES

last_alert_time = 0

def show_alert(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Battery Alert", 1)


def check_alerts(data):
    global last_alert_time

    percent = data["percent"]
    plugged = data["plugged"]

    # 🔋 LOW BATTERY
    if percent <= LOW_BATTERY_THRESHOLD and not plugged:
        show_alert(f"⚠️ Battery low: {percent}%")

    # ⚡ FULL CHARGE
    if percent >= 95 and plugged:
        show_alert("🔌 Battery almost full! Consider unplugging.")

    # 🧠 SMART PREDICTION
    time_left = estimate_time_remaining(percent)

    if time_left and time_left < SMART_ALERT_MINUTES and not plugged:
        show_alert(f"⚠️ Battery may die in {int(time_left)} minutes!")