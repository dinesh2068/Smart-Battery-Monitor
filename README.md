# Smart Battery Monitor for Windows:

A real-time battery monitoring and analytics tool built using Python.
Tracks battery usage, logs historical data, provides alerts, and visualizes trends via a web dashboard.

---

## Features

* Real-time battery status (charging/discharging)
* Historical battery tracking using SQLite
* Interactive web dashboard (Chart.js)
* Smart alerts (low battery, full charge, time prediction)
* Battery health estimation
* Runs in background (daemon-style pipeline)
* Auto-start with Windows

---

## Tech Stack

* Python
* Flask (Web Dashboard)
* SQLite (Data Storage)
* psutil (System Monitoring)
* Chart.js (Frontend Visualization)
* PyWebView (Desktop App Wrapper)

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/battery-monitor.git
cd battery-monitor
pip install -r requirements.txt
```

---

## Run

```bash
python app.py
```

---

## How It Works

1. Background pipeline collects battery data every few seconds
2. Data is stored in SQLite database
3. Alerts are triggered based on conditions
4. Flask dashboard displays real-time + historical data

---

## Note

* Works on Windows (uses system battery APIs)
* Battery health estimation may vary by hardware

---

## Future Improvements

* WMI-based accurate battery metrics
* ML-based battery degradation prediction
* Cross-platform support (Linux/macOS)

---

## Author

Created by DINESHKARTHIK N – 2026 <br>
Feel free to contribute or fork the project!