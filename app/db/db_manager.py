
import sqlite3
from datetime import datetime
import random

DB_PATH = "app/db/traffic_system.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def add_intersection(name, location):
    with get_connection() as conn:
        conn.execute("INSERT INTO intersections (name, location) VALUES (?, ?)", (name, location))
        conn.commit()

def log_incident(intersection_id, type_, lane, image_folder):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO incidents (intersection_id, timestamp, type, lane, image_folder) VALUES (?, ?, ?, ?, ?)",
            (intersection_id, datetime.now().isoformat(), type_, lane, image_folder)
        )
        conn.commit()

def get_active_incidents():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM incidents WHERE status = 'open'").fetchall()

def close_incident(incident_id):
    with get_connection() as conn:
        conn.execute("UPDATE incidents SET status = 'closed' WHERE id = ?", (incident_id,))
        conn.commit()

def add_officer(name, zone, phone):
    with get_connection() as conn:
        conn.execute("INSERT INTO officers (name, zone, phone) VALUES (?, ?, ?)", (name, zone, phone))
        conn.commit()

def get_on_call_officers():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM officers WHERE is_on_call = 1").fetchall()

# === Audit Logging ===
def log_system_event(event_type, description):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO system_logs (timestamp, event_type, description) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), event_type, description)
        )
        conn.commit()

def get_recent_logs(limit=50):
    with get_connection() as conn:
        return conn.execute(
            "SELECT timestamp, event_type, description FROM system_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
        
def insert_random_officer():
    with get_connection() as conn:
        names = ["Ahmad", "Nour", "Zein", "Rami", "Lara", "Maya"]
        zones = ["North", "South", "East", "West"]
        name = random.choice(names)
        zone = random.choice(zones)
        phone = f"03-{random.randint(100000, 999999)}"

        conn.execute("""
            INSERT INTO officers (name, zone, phone, is_on_call)
            VALUES (?, ?, ?, 1)
        """, (name, zone, phone))
        conn.commit()

