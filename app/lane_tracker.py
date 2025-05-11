import json
import os
from threading import Lock

LANE_COUNT_PATH = "app/state/lane_counts.json"
lane_lock = Lock()

def update_lane_count(lane, count):
    with lane_lock:
        try:
            if os.path.exists(LANE_COUNT_PATH):
                with open(LANE_COUNT_PATH, "r") as f:
                    data = json.load(f)
            else:
                data = {}

            data[lane] = count

            with open(LANE_COUNT_PATH, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Failed to update lane count: {e}")

def load_lane_counts():
    if not os.path.exists(LANE_COUNT_PATH):
        return {"north": 0, "south": 0, "east": 0, "west": 0}
    with open(LANE_COUNT_PATH, "r") as f:
        return json.load(f)
