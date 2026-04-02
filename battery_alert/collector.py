import psutil
from datetime import datetime

def get_battery_data():
    battery = psutil.sensors_battery()

    if battery is None:
        return None

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "percent": battery.percent,
        "plugged": int(battery.power_plugged)
    }