
from pynput.mouse import Listener
from datetime import datetime
import requests
import json
import hashlib
import hmac
import base64
import threading
import time
import psutil

# Azure Log Analytics Workspace details
WORKSPACE_ID = "your-workspace-id"  # Replace with your Workspace ID
PRIMARY_KEY = "your-primary-key"    # Replace with your Primary Key
LOG_TYPE = "ActivityLogs"           # Log table name in Azure

# Global variables for mouse tracking
mouse_data = {"count": 0, "positions": set()}
LOCK = threading.Lock()

# Azure signature generation
def build_signature(date, content_length, method, content_type, resource):
    x_headers = f'x-ms-date:{date}'
    string_to_hash = f'{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}'
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(PRIMARY_KEY)
    encoded_hash = hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
    return f"SharedKey {WORKSPACE_ID}:{base64.b64encode(encoded_hash).decode()}"

# Send logs to Azure
def send_to_azure(logs):
    body = json.dumps(logs)
    uri = f'https://{WORKSPACE_ID}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01'
    date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    signature = build_signature(date, len(body), 'POST', 'application/json', f'/api/logs')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': signature,
        'Log-Type': LOG_TYPE,
        'x-ms-date': date,
    }
    response = requests.post(uri, data=body, headers=headers)
    if response.status_code >= 200 and response.status_code <= 299:
        print("Logs successfully sent to Azure")
    else:
        print(f"Failed to send logs: {response.status_code} - {response.text}")

# Aggregated mouse data logging
def log_mouse_data():
    while True:
        time.sleep(15)  # Log every 15 seconds
        LOCK.acquire()
        try:
            if mouse_data["count"] > 0:
                logs = [{
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "movement_count": mouse_data["count"],
                    "distinct_positions": len(mouse_data["positions"])
                }]
                send_to_azure(logs)
                mouse_data["count"] = 0
                mouse_data["positions"] = set()
        finally:
            LOCK.release()

# Mouse movement listener
def on_move(x, y):
    LOCK.acquire()
    try:
        mouse_data["count"] += 1
        mouse_data["positions"].add((round(x), round(y)))
    finally:
        LOCK.release()

# System usage logging
def log_system_usage():
    while True:
        time.sleep(15)  # Log every 15 seconds
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        logs = [{
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "cpu_usage": cpu,
            "memory_usage": memory
        }]
        send_to_azure(logs)

# Main function
def main():
    threading.Thread(target=log_mouse_data, daemon=True).start()
    threading.Thread(target=log_system_usage, daemon=True).start()
    print("Starting mouse activity logging...")
    with Listener(on_move=on_move) as listener:
        listener.join()

if __name__ == "__main__":
    main()
