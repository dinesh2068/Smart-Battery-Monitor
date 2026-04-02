import psutil
from datetime import datetime

def get_battery_data():
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    secs = battery.secsleft
    minutes_left = None

    # Only valid if secsleft is positive
    if secs and secs > 0:
        minutes_left = int(secs / 60)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "percent": battery.percent,
        "plugged": int(battery.power_plugged),
        "minutes_left": minutes_left
    }