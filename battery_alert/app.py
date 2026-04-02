import webview
import threading
from web_dashboard import app
from main import run

def start_pipeline():
    run()

def start_flask():
    app.run()

if __name__ == '__main__':
    t1 = threading.Thread(target=start_pipeline)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=start_flask)
    t2.daemon = True
    t2.start()

    webview.create_window("Battery Monitor", "http://127.0.0.1:5000")
    webview.start()