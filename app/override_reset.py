import time
import threading
from app import state

RESET_INTERVAL = 5           # check every 5 seconds
EMERGENCY_TIMEOUT = 10       # clear override after 10s of no emergency

def monitor_override():
    while True:
        if state.override_state.get("manual_override"):
            # Compare to last YOLO detection heartbeat
            last_seen = state.system_status.get("last_yolo_heartbeat", 0)
            now = time.time()

            if now - last_seen > EMERGENCY_TIMEOUT:
                print("[OVERRIDE RESET] No emergency seen, override cleared.")
                state.override_state["manual_override"] = False
                state.override_state["forced_lane"] = None
                state.system_status["last_override_reason"] = "Auto-reset after inactivity"

        time.sleep(RESET_INTERVAL)

def start_override_monitor():
    t = threading.Thread(target=monitor_override, daemon=True)
    t.start()
