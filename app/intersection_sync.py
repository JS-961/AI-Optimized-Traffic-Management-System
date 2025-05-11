# app/intersection_sync.py

import os
import json

INTERSECTIONS_DIR = "app/state/intersections"

def read_all_intersection_states():
    all_states = {}
    if not os.path.exists(INTERSECTIONS_DIR):
        os.makedirs(INTERSECTIONS_DIR)
        return all_states

    for filename in os.listdir(INTERSECTIONS_DIR):
        if filename.endswith(".json"):
            path = os.path.join(INTERSECTIONS_DIR, filename)
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    intersection_id = os.path.splitext(filename)[0]
                    all_states[intersection_id] = data
            except Exception as e:
                print(f"[ERROR] Failed to load {filename}: {e}")
    return all_states
