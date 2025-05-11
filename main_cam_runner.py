# main_cam_runner.py

import cv2
import time
from threading import Thread
from app.camera_registry import camera_registry
from app.yolo_detector import YOLODetector
from app.vehicle_processor import VehicleProcessor
from app import state

# === Setup ===
frame_width, frame_height = 640, 480
detector = YOLODetector(conf_threshold=0.3)
processor = VehicleProcessor(frame_width, frame_height)

def draw_beautiful_label(frame, label_text, x, y, color=(0, 255, 0)):
    (text_width, text_height), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y - text_height - 10), (x + text_width + 4, y + baseline - 4), (0, 0, 0), -1)
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, label_text, (x + 2, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def process_camera(cam):
    cap = cv2.VideoCapture(cam["source"])
    zone = cam["zone"]
    cam_id = cam["camera_id"]

    prev_frame_time = 0

    while cap.isOpened():
        try:
            ret, frame = cap.read()
            if not ret:
                print(f"[ERROR] Failed to read from camera {zone}")
                break

            frame = cv2.resize(frame, (frame_width, frame_height))
            detections = detector.detect(frame)

            for detection in detections:
                class_name = detection['class']
                conf = detection['conf']
                bbox = detection['bbox']
                x1, y1, x2, y2 = map(int, bbox)
                is_emergency = detection.get("emergency", False)
                box_color = (0, 0, 255) if is_emergency else (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                label = f"{class_name} {conf:.2f}"
                draw_beautiful_label(frame, label, x1, y1, color=box_color)

            count = processor.count_vehicles_in_zone(detections, zone)
            state.lane_counts[zone] = count
            state.system_status["last_yolo_heartbeat"] = time.time()

            # FPS
            new_frame_time = time.time()
            fps = 1 / (new_frame_time - prev_frame_time) if (new_frame_time - prev_frame_time) > 0 else 0
            prev_frame_time = new_frame_time

            zone_text = f"{zone.upper()} ({cam_id}) - Vehicles: {count} - FPS: {int(fps)}"
            cv2.putText(frame, zone_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.imshow(f"Feed: {zone}", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            print(f"[CAMERA THREAD ERROR - {zone}] {e}")
            break

    cap.release()
    cv2.destroyWindow(f"Feed: {zone}")

# === Launch all camera threads ===
threads = []
for cam in camera_registry:
    t = Thread(target=process_camera, args=(cam,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

cv2.destroyAllWindows()
