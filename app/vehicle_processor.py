from app import state

class VehicleProcessor:
    def __init__(self, width, height):
        self.frame_width = width
        self.frame_height = height

    def count_vehicles_per_lane(self, detections):
        """
        Classify each detection into a directional lane
        based on its center position in the frame.
        """
        counts = {"north": 0, "south": 0, "east": 0, "west": 0}
        for d in detections:
            x1, y1, x2, y2 = d["bbox"]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if cx < self.frame_width // 2 and cy < self.frame_height // 2:
                counts["north"] += 1
            elif cx > self.frame_width // 2 and cy < self.frame_height // 2:
                counts["east"] += 1
            elif cx < self.frame_width // 2 and cy > self.frame_height // 2:
                counts["west"] += 1
            else:
                counts["south"] += 1
        return counts

    def count_vehicles_in_zone(self, detections, zone):
        """
        Get count of vehicles for a single zone, based on full-frame quadrant logic.
        If an emergency vehicle is detected in the zone, trigger an override.
        """
        lane_counts = self.count_vehicles_per_lane(detections)
        vehicle_count = lane_counts.get(zone, 0)

        emergency_detected = any(
            d["class"].lower() in ["ambulance", "fire_truck", "police_car"]
            and self.get_lane_from_center(d["bbox"]) == zone
            for d in detections
        )


        if emergency_detected:
            if not state.override_state.get("manual_override") or state.override_state.get("forced_lane") != zone:
                state.override_state["manual_override"] = True
                state.override_state["forced_lane"] = zone
                state.system_status["last_override_reason"] = f"Emergency vehicle detected in {zone}"
                print(f"[EMERGENCY OVERRIDE] Priority given to {zone} lane")

        return vehicle_count

    def get_lane_from_center(self, bbox):
        """
        Helper to determine lane from bounding box center.
        """
        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        if cx < self.frame_width // 2 and cy < self.frame_height // 2:
            return "north"
        elif cx > self.frame_width // 2 and cy < self.frame_height // 2:
            return "east"
        elif cx < self.frame_width // 2 and cy > self.frame_height // 2:
            return "west"
        else:
            return "south"
