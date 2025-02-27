from flask import Flask, render_template, jsonify
import socket
import threading
import json
import logging
from datetime import datetime

app = Flask(__name__)
alerts = []  # List to store alerts
lock = threading.Lock()  # Lock to synchronize access to alerts list

# Set up logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def socket_server():
    """Socket server to receive alerts from external clients"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 5050))
    server.listen(5)
    logging.info("[SERVER] Waiting for alerts...")

    while True:
        client, addr = server.accept()
        logging.info(f"[SERVER] Connection established with {addr}")
        
        try:
            data = client.recv(1024).decode("utf-8")
            if data:
                alert = json.loads(data)
                alert["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with lock:  # Acquire lock before modifying the list
                    alerts.append(alert)
                    print("[ALERT RECEIVED AND APPENDED]", alert)  
                    print("[CURRENT ALERTS LIST]", alerts)  
                    logging.info("[ALERT RECEIVED] %s", alert)
        except Exception as e:
            logging.error(f"Error while processing alert: {e}")
            print(f"Error while processing alert: {e}")
        finally:
            client.close()

@app.route('/')
def dashboard():
    """Render the dashboard with alerts"""
    logging.info("Dashboard accessed")
    return render_template("dashboard.html", alerts=alerts)

@app.route('/alerts')
def get_alerts():
    """API route to get alerts in JSON format"""
    logging.info("Alerts accessed")
    with lock:  # Acquire lock before reading the list
        current_alerts = alerts[::-1]  # Reverse order
    print("[DEBUG] Alerts accessed. Current alerts:", current_alerts)
    return jsonify(current_alerts)

if __name__ == '__main__':
    logging.info("Application started")
    print("Application started at http://127.0.0.1:5000")
    threading.Thread(target=socket_server, daemon=True).start()
    app.run(debug=True, port=5000, use_reloader=False)