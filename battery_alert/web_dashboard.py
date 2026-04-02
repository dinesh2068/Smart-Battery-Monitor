from flask import Flask, jsonify
from analyzer import get_real_battery_health
import sqlite3

app = Flask(__name__)
DB_PATH = "data/battery.db"

@app.route("/data")
def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, percent, plugged FROM battery_logs ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)

@app.route("/health")
def battery_health():
    health = get_real_battery_health()

    if health is None:
        health = 0

    return {
    "health": int(health),
    "status": "good" if health > 80 else "moderate"
    }

latest_alert = ""

@app.route("/alert")
def get_alert():
    return {"alert": latest_alert}

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Battery Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body style="
        background: linear-gradient(135deg, #0f172a, #020617);
        color: #e2e8f0;
        font-family: 'Segoe UI';
        padding: 20px;
    ">

    <h1 style="font-size: 28px;">🔋 Battery Monitor</h1>

    <div style="
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    ">

        <div style="background:#020617; padding:15px; border-radius:10px;">
            <h3 id="status">Status</h3>
        </div>

        <div style="background:#020617; padding:15px; border-radius:10px;">
            <h3 id="percent">Battery</h3>
        </div>

        <div style="background:#020617; padding:15px; border-radius:10px;">
            <h3 id="health">Health</h3>
        </div>
        <h3 id="alert" style="color: orange;"></h3>

    </div>

    <canvas id="chart"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <script>
            let chart;

            async function loadData() {
                const res = await fetch('/data');
                const data = await res.json();

                const labels = data.map(x => x[0]);
                const values = data.map(x => x[1]);

                return { labels, values, raw: data };
            }

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
                                maxTicksLimit: 8   // 🔥 reduces clutter
                            }
                        }
                    }
                }
            });
            }
            
            async function updateHealth() {
            const res = await fetch('/health');
            const data = await res.json();

            document.getElementById("health").innerText =
                "Health: " + data.health + "%";
            }

            async function updateChart() {
                const { labels, values, raw } = await loadData();

                chart.data.labels = labels;
                chart.data.datasets[0].data = values;
                chart.update();

                // 🔥 NEW: Show latest status
                const latest = raw[raw.length - 1];
                const percent = latest[1];
                const plugged = latest[2];

                document.getElementById("percent").innerText = `Battery: ${percent}%`;
                document.getElementById("status").innerText =
                    plugged === 1 ? "Status: ⚡ Charging" : "Status: 🔋 Discharging";
            }

            async function updateAlert() {
            const res = await fetch('/alert');
            const data = await res.json();

            document.getElementById("alert").innerText = data.alert || "";
            }

            setInterval(updateAlert, 2000);

            renderChart();
            setInterval(updateChart, 2000);
            setInterval(updateHealth, 5000);
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)