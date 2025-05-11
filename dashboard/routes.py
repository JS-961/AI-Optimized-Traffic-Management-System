import sys
import os
from app.lane_tracker import load_lane_counts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, render_template, jsonify, request, send_file, session, redirect, url_for
from app import state
from app.db.db_manager import (
    get_active_incidents,
    get_on_call_officers,
    log_incident,
    log_system_event,
    get_recent_logs,
    insert_random_officer
)
from app.intersection_sync import read_all_intersection_states
from io import BytesIO
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

# Secure cookie flags
app.config.update({
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SECURE': False
})

USERNAME = 'admin'
PASSWORD = 'admin123'
API_SECRET = "admin123"

@app.before_request
def check_api_token():
    if request.path.startswith("/api"):
        if session.get("logged_in"):
            return
        token = request.headers.get("X-API-KEY")
        if token != API_SECRET:
            return jsonify({"error": "Unauthorized"}), 401

@app.route("/")
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'attempts' not in session:
        session['attempts'] = 0

    if request.method == "POST":
        session['attempts'] += 1
        username = request.form.get("username")
        password = request.form.get("password")

        if session['attempts'] > 5:
            return render_template("login.html", error="Too many login attempts. Try again later.")

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            session['attempts'] = 0
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/api/status")
def get_status():
    lane_counts = load_lane_counts()
    return jsonify({
        "lane_counts": lane_counts,
        "override": state.override_state,
        "mode": state.system_status.get("mode", "UNKNOWN"),
        "last_heartbeat": state.system_status.get("last_yolo_heartbeat")
    })

@app.route("/api/set_mode", methods=["POST"])
def set_mode():
    data = request.json
    mode = data.get("mode", "").upper()

    if mode not in ["AI", "MANUAL", "FAILSAFE"]:
        return jsonify({"error": "Invalid mode"}), 400

    state.system_status["mode"] = mode
    log_system_event("mode_change", f"System mode manually set to {mode}")
    return jsonify({"success": True, "mode": mode})

@app.route("/api/override", methods=["POST"])
def set_override():
    data = request.json
    enabled = data.get("enabled", False)
    lane = data.get("lane")
    state.override_state["manual_override"] = enabled
    state.override_state["forced_lane"] = lane if enabled else None
    log_system_event("override", f"{'enabled' if enabled else 'disabled'} → {lane if enabled else 'none'}")
    return jsonify({"success": True, "override": state.override_state})

@app.route("/api/incidents")
def incidents():
    data = get_active_incidents()
    return jsonify([{
        "id": row[0],
        "intersection_id": row[1],
        "timestamp": row[2],
        "type": row[3],
        "lane": row[4],
        "folder": row[5]
    } for row in data])

@app.route("/api/officers")
def officers():
    data = get_on_call_officers()
    return jsonify([{
        "id": row[0],
        "name": row[1],
        "zone": row[2],
        "phone": row[3],
        "on_call": bool(row[4])
    } for row in data])

@app.route("/api/add_officer", methods=["POST"])
def add_random_officer():
    new_id = insert_random_officer()
    log_system_event("admin_action", f"Added new random officer with ID {new_id}")
    return jsonify({"success": True, "id": new_id})

@app.route("/api/recommendation")
def recommendation():
    lane_counts = state.lane_counts
    if all(v == 0 for v in lane_counts.values()):
        return jsonify({"lane": None, "count": 0})
    best_lane = max(lane_counts, key=lane_counts.get)
    return jsonify({"lane": best_lane, "count": lane_counts[best_lane]})

@app.route("/api/simulate_violation", methods=["POST"])
def simulate_violation():
    lanes = ["north", "south", "east", "west"]
    random_lane = random.choice(lanes)
    folder = f"demo_incident_{random.randint(1000, 9999)}"
    log_incident(intersection_id=1, type_="simulated_violation", lane=random_lane, image_folder=folder)
    log_system_event("demo", f"Simulated violation on lane {random_lane}")
    return jsonify({"success": True, "lane": random_lane})

@app.route("/api/export_report")
def export_report():
    rows = get_active_incidents()
    text_data = "ID,Intersection,Timestamp,Type,Lane,Folder,Status\n"
    for row in rows:
        text_data += ",".join(map(str, row)) + "\n"
    csv_buffer = BytesIO()
    csv_buffer.write(text_data.encode("utf-8"))
    csv_buffer.seek(0)
    log_system_event("export", "CSV incident report generated")
    return send_file(csv_buffer, mimetype="text/csv", download_name="incident_report.csv", as_attachment=True)

@app.route("/api/logs")
def fetch_logs():
    logs = get_recent_logs()
    return jsonify([
        {"timestamp": ts, "event_type": etype, "description": desc}
        for ts, etype, desc in logs
    ])

@app.route("/api/export_lane_history")
def export_lane_history():
    from_path = "app/state/lane_traffic_log.csv"
    if not os.path.exists(from_path):
        return jsonify({"error": "No history available"}), 404
    return send_file(from_path, mimetype="text/csv", download_name="lane_history.csv", as_attachment=True)

@app.route("/api/intersections")
def get_all_intersections():
    return jsonify(read_all_intersection_states())

if __name__ == "__main__":
    app.run(debug=False)
