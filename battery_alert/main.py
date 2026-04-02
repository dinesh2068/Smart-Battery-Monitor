import time
from collector import get_battery_data
from database import init_db, insert_data
from alerts import check_alerts
from utils import setup_logger, log
from config import INTERVAL
import os

def run():
    setup_logger()
    init_db()

    while True:
        data = get_battery_data()

        if data:
            print(f"[LOG] {data}")
            log(str(data))
            insert_data(data)
            check_alerts(data)

        time.sleep(INTERVAL)


def generate_battery_report():
    os.system("powercfg /batteryreport /output battery_report.html")

if __name__ == "__main__":
    run()