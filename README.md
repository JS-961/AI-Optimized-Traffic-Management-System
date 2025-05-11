# 🚦 AI-Powered Traffic Management System

This is a full-stack, real-time traffic control system built using computer vision, Flask, YOLOv8, SQLite, and a live admin dashboard. Designed to optimize traffic signal behavior, prioritize emergency vehicles, detect red-light violations, and assist traffic administrators with real-time control and oversight.

---

## 📌 Project Overview

This project simulates an intelligent traffic intersection control system using Raspberry Pi (for deployment), Python, and a browser-based dashboard. It includes:

- Real-time vehicle detection using YOLOv8
- Smart traffic signal selection based on congestion
- Emergency vehicle override with delay buffer
- Red-light violation detection and evidence capture
- Full administrative dashboard with live analytics
- System audit logs for traceability
- Simulated intersection view and demo tools

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| AI/Detection | YOLOv8 via Ultralytics |
| Database | SQLite |
| Dashboard | HTML + CSS + JS (Vanilla) |
| Visualization | Leaflet.js, Animated HTML UI |
| Video Capture | OpenCV |
| Runtime | Raspberry Pi (target), Windows/Linux (dev) |

---

## 🧠 System Architecture

### 📷 Input
- One or more video feeds (e.g., USB cam, IP cam)
- YOLOv8 detects vehicles per frame

### 🧮 Processing
- `VehicleProcessor` assigns vehicle detections to lanes
- `TrafficLightController` dynamically selects the active green lane
- Emergency detection temporarily overrides normal flow
- Red-light violators are captured and logged with screenshots

### 🖥️ Output
- Flask API updates shared `state`
- Live dashboard fetches API data every 5s
- Admin can override signals or simulate conditions
- Logs and violations are stored and exported

---

## 🗂️ Project Structure

```
ai_traffic_system/
├── app/
│   ├── camera_registry.py         # Multi-camera config
│   ├── camera_handler.py          # OpenCV camera manager
│   ├── yolo_detector.py           # YOLOv8 wrapper
│   ├── vehicle_processor.py       # Assign detections to lanes
│   ├── traffic_light_controller.py# Traffic signal logic + override
│   ├── state.py                   # Shared memory across modules
│   └── db/
│       ├── db_manager.py          # All DB functions
│       └── traffic_system.db      # SQLite DB
│
├── dashboard/
│   ├── templates/
│   │   └── index.html             # Admin dashboard UI
│   └── routes.py                  # API and page logic
│
├── simulation/
│   └── traffic_sim.py             # Legacy (Pygame) sim (optional)
├── multi_cam_run.py               # Multi-camera YOLO inference runner
├── run.py                         # Single-camera entry point
├── run_dashboard.py               # Launch Flask server
├── init_db.py                     # Sets up DB tables
```

---

## 🧪 Key Features

### 🧠 AI-Powered Vehicle Detection
- YOLOv8 runs on every frame
- Vehicle bounding boxes classified into directions (north, south, etc.)

### 🚦 Smart Signal Control
- Lanes with the highest car count are prioritized
- A failsafe kicks in if no dominant lane exists
- Manual override via dashboard

### 🚨 Emergency Vehicle Priority
- Detected via input trigger or simulation
- Overrides current cycle with a delay buffer
- Deactivates automatically when vehicle exits frame

### 🚫 Red Light Violation Detection
- Triggers when car crosses stop line on red
- Screenshot evidence captured
- Incident logged to database
- Can be simulated via admin panel

### 📤 CSV Report Export
- Incidents exportable via dashboard
- Preformatted with ID, timestamp, lane, folder, etc.

### 🧾 System Audit Logs
- Every event is tracked:
  - Override toggles
  - Violation triggers
  - Export actions
  - Emergency activations
- Logs viewable in dashboard

### 🌍 Real-Time Intersection View
- Leaflet.js map of Gemmayzeh intersection
- Directional camera markers
- Simulated lane activation with animated lights

---

## 💻 Demo Tools

Use these from the dashboard to simulate events:

| Tool | Action |
|------|--------|
| ✅ Simulate Violation | Fakes a red-light run |
| ✅ Force Override | Picks a green lane manually |
| ✅ Export CSV | Downloads report for all active incidents |

---

## 🧱 Simulated Intersection View

A lightweight animated panel is embedded in the dashboard that:

- Mimics a 4-way intersection
- Lights update in real-time based on system state
- Provides a visual alternative to Unity or SUMO

---

## ⚙️ Setup & Run

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```

2. Run YOLO on live camera:
   ```
   python multi_cam_run.py
   ```

3. Launch dashboard:
   ```
   python run_dashboard.py
   ```

4. Initialize database (first time only):
   ```
   python init_db.py
   ```

---

## ✅ Status Summary

| Module | Status |
|--------|--------|
| AI Detection | ✅ Complete |
| Traffic Logic | ✅ Complete |
| Emergency Flow | ✅ Complete |
| Red-Light Capture | ✅ Complete |
| Admin UI | ✅ Complete |
| Multi-Cam Support | ✅ Complete |
| Map Anchoring | ✅ Complete |
| Audit Logs | ✅ Complete |
| Demo Mode | ✅ Complete |
| 3D Model | 🚧 Replaced with animated HTML |

---

## 🧠 Author Notes

- Project based on the real-world intersection in Gemmayzeh, Beirut
- Designed for deployment on Raspberry Pi 5 (8 GB)
- Intended as a prototype for scalable AI traffic control

---

## 📜 License
This project is part of a university capstone and is shared for academic demonstration purposes.
