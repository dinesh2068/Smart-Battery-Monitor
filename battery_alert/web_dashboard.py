from flask import Flask, jsonify
from collector import get_battery_data
from analyzer import get_real_battery_health
from analyzer import estimate_time_remaining
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "data/battery.db"

# 📊 TODAY DATA ONLY
@app.route("/data")
def get_data():
    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp, percent, plugged
    FROM battery_logs
    WHERE DATE(timestamp) = ?
    ORDER BY id ASC
    """, (today,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)

# ⚡ LIVE DATA
@app.route("/live")
def live_data():
    data = get_battery_data()

    time_left = estimate_time_remaining()

    return {
        "percent": data["percent"],
        "plugged": data["plugged"],
        "minutes_left": time_left
    }

# 🔋 HEALTH
@app.route("/health")
def battery_health():
    health = get_real_battery_health()
    return {"health": int(health) if health else 0}

# 🌐 UI
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Battery Monitor</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body style="
background: linear-gradient(135deg, #0f172a, #020617);
color: #e2e8f0;
font-family: 'Segoe UI';
padding: 20px;
">

<h1>🔋 Battery Monitor</h1>

<div style="display:flex; gap:20px; margin-bottom:20px;">
    <div style="background:#020617; padding:15px; border-radius:10px;">
        <h3 id="status">Status</h3>
    </div>

    <div style="background:#020617; padding:15px; border-radius:10px;">
        <h3 id="percent">Battery</h3>
    </div>

    <div style="background:#020617; padding:15px; border-radius:10px;">
        <h3 id="health">Health</h3>
    </div>
</div>

<canvas id="chart"></canvas>

<script>
let chart;

// 🔥 FORMAT TIME
function formatMinutes(mins) {
    if (!mins || mins <= 0) return "";

    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;

    if (hours > 0) {
        return minutes === 0 
            ? `${hours} hr`
            : `${hours} hr ${minutes} min`;
    } else {
        return `${minutes} min`;
    }
}

// 📊 LOAD GRAPH
async function loadData() {
    const res = await fetch('/data');
    const data = await res.json();

    return {
        labels: data.map(x => x[0]),
        values: data.map(x => x[1])
    };
}

// ⚡ LIVE DATA
async function getLive() {
    const res = await fetch('/live');
    return await res.json();
}

// 🔋 HEALTH
async function getHealth() {
    const res = await fetch('/health');
    return await res.json();
}

// 📈 RENDER CHART
async function renderChart() {
    const ctx = document.getElementById('chart').getContext('2d');
    const { labels, values } = await loadData();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Battery %',
                data: values,
                borderWidth: 2,
                tension: 0.3,
                pointRadius: 2
            }]
        },
        options: {
            scales: {
                x: {
                    ticks: {
                        maxTicksLimit: 8
                    }
                }
            }
        }
    });
}

// 🔄 UPDATE GRAPH
async function updateChart() {
    const { labels, values } = await loadData();
    chart.data.labels = labels;
    chart.data.datasets[0].data = values;
    chart.update();
}

// 🔄 UPDATE STATUS
async function updateStatus() {
    const live = await getLive();
    const health = await getHealth();

    const timeText = formatMinutes(live.minutes_left);

    document.getElementById("percent").innerText =
        `Battery: ${live.percent}%`;

    document.getElementById("health").innerText =
        `Health: ${health.health}%`;

    if (live.plugged === 1) {
        document.getElementById("status").innerText =
            "⚡ Charging";  // ❌ NO fake time
    } else {
        document.getElementById("status").innerText =
            live.minutes_left
            ? `🔋 Discharging (${formatMinutes(live.minutes_left)} left)`
            : "🔋 Discharging";
    }
}

// 🚀 INIT
renderChart();
setInterval(updateChart, 5000);
setInterval(updateStatus, 2000);

</script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)