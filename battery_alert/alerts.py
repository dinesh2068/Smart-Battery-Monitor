import ctypes
import time

last_alert_percent = None
last_alert_time = 0

COOLDOWN = 300  # 5 minutes

def show_alert(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Battery Alert", 1)

def check_alerts(data):
    global last_alert_percent, last_alert_time

    percent = data["percent"]
    plugged = data["plugged"]
    now = time.time()

    # Skip alerts if charging
    if plugged:
        return

    # Low battery alert every 5%
    if percent <= 30:
        if last_alert_percent is None or percent <= last_alert_percent - 5:
            if now - last_alert_time > COOLDOWN:
                show_alert(f"⚠️ Battery low: {percent}% remaining")
                last_alert_percent = percent
                last_alert_time = now

    # Critical alert
    if percent <= 10:
        if now - last_alert_time > 60:
            show_alert("🚨 CRITICAL BATTERY! Plug in now!")
            last_alert_time = now