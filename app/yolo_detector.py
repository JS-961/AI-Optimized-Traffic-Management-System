from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, coco_model_path="models/yolov8n.pt", emergency_model_path="models/yolov8n_emergency.pt", conf_threshold=0.4):
        try:
            self.coco_model = YOLO(coco_model_path)
            self.emergency_model = YOLO(emergency_model_path)
        except Exception as e:
            print(f"[YOLO LOAD ERROR] {e}")
            self.coco_model, self.emergency_model = None, None

        self.conf_threshold = conf_threshold
        self.coco_classes = [2, 3, 5, 7]  # COCO vehicles
        self.emergency_classes = [0, 1, 2]  # Roboflow-trained emergency vehicles

    def detect(self, frame):
        if self.coco_model is None or self.emergency_model is None:
            return []

        resized = cv2.resize(frame, (640, 480))
        detections = []

        coco_results = self.coco_model.predict(source=resized, conf=self.conf_threshold, classes=self.coco_classes, verbose=False)
        for r in coco_results:
            for i in range(len(r.boxes.cls)):
                cls_id = int(r.boxes.cls[i])
                conf = float(r.boxes.conf[i])
                xyxy = r.boxes.xyxy[i].tolist()
                label = self.coco_model.names[cls_id]
                detections.append({
                    'class': label,
                    'conf': conf,
                    'bbox': xyxy
                })

        emergency_results = self.emergency_model.predict(source=resized, conf=self.conf_threshold, verbose=False)
        for r in emergency_results:
            for i in range(len(r.boxes.cls)):
                cls_id = int(r.boxes.cls[i])
                conf = float(r.boxes.conf[i])
                xyxy = r.boxes.xyxy[i].tolist()
                label = self.emergency_model.names[cls_id]
                detections.append({
                    'class': label,
                    'conf': conf,
                    'bbox': xyxy
                })

        return detections
