# app/csv_logger.py

import csv
import time
import os
from datetime import datetime
from threading import Thread
from app import state

CSV_PATH = "app/state/lane_traffic_log.csv"

def start_logger():
    def loop():
        while True:
            try:
                row = [datetime.now().isoformat()] + [state.lane_counts[l] for l in ["north", "south", "east", "west"]]
                write_row(row)
            except Exception as e:
                print(f"[CSV LOGGER ERROR] {e}")
            time.sleep(5)  # log every 5 seconds

    Thread(target=loop, daemon=True).start()

def write_row(data):
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)  # <-- REQUIRED
    exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "north", "south", "east", "west"])
        writer.writerow(data)
