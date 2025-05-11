# app/intersection_manager.py

import threading
import time
import json
import os
from app import state

SHARED_FILE = "shared/intersections.json"
INTERSECTION_ID = "GEMMAYZEH"  # unique ID per intersection

def write_own_status():
    entry = {
        "id": INTERSECTION_ID,
        "timestamp": time.time(),
        "lane_counts": state.lane_counts,
        "override": state.override_state
    }

    try:
        if os.path.exists(SHARED_FILE):
            with open(SHARED_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data[INTERSECTION_ID] = entry

        with open(SHARED_FILE, "w") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"[INTERSECTION WRITE ERROR] {e}")

def read_all_other_intersections():
    try:
        with open(SHARED_FILE, "r") as f:
            data = json.load(f)

        return {k: v for k, v in data.items() if k != INTERSECTION_ID}
    except Exception:
        return {}

def coordination_loop():
    while True:
        write_own_status()
        others = read_all_other_intersections()

        # Example: print most congested intersection
        if others:
            worst = max(others.values(), key=lambda i: sum(i['lane_counts'].values()))
            print(f"[MULTI-INTXN] Most congested: {worst['id']}")

        time.sleep(5)

def start_intersection_sync():
    t = threading.Thread(target=coordination_loop, daemon=True)
    t.start()
