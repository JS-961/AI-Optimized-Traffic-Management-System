# AI-Optimized Traffic Management System

An AI-driven, real-time traffic control system leveraging computer vision, Flask, YOLOv8, SQLite, and a live admin dashboard. Designed to optimize traffic signal behavior, prioritize emergency vehicles, detect red-light violations, and assist traffic administrators with real-time control and oversight.

---

## 🚦 Project Overview

This project simulates an intelligent traffic intersection control system with the following features:

* **Real-time vehicle detection** using YOLOv8 and OpenCV.
* **Dynamic traffic signal control** based on live traffic density.
* **Emergency vehicle prioritization** through manual overrides.
* **Red-light violation detection** with incident logging.
* **Interactive dashboard** for monitoring and control.
* **Data logging** for traffic analysis and reporting.

---

## 🧰 Technologies Used

* **Backend**: Python, Flask
* **Computer Vision**: OpenCV, YOLOv8
* **Database**: SQLite
* **Frontend**: HTML, CSS, JavaScript, Leaflet.js
* **Visualization**: Leaflet.js for map integration

---

## 📁 Project Structure

```
ai_traffic_system/
├── app/
│   ├── camera.py
│   ├── intersection_sync.py
│   └── ...
├── dashboard/
│   ├── routes.py
│   └── ...
├── static/
│   ├── style.css
│   └── ...
├── templates/
│   ├── index.html
│   └── ...
├── models/
│   └── yolov8n.pt
├── logs/
│   └── lane_traffic_log.csv
├── run_dashboard.py
├── run_camera.py
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* pip

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JS-961/AI-Optimized-Traffic-Management-System.git
   cd AI-Optimized-Traffic-Management-System
   ```



2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```



3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```



4. **Download YOLOv8 model weights:**

   Place the `yolov8n.pt` model file into the `models/` directory. You can download it from the [Ultralytics YOLOv8 repository](https://github.com/ultralytics/yolov8).

---

## 🧪 Running the Application

1. **Start the camera processing module:**

   ```bash
   python run_camera.py
   ```



2. **Start the Flask dashboard:**

   ```bash
   python run_dashboard.py
   ```



3. **Access the dashboard:**

   Open your web browser and navigate to `http://localhost:5000`.

---

## 📊 Dashboard Features

* **Live Lane Status**: Displays real-time vehicle counts per lane.
* **Emergency Override**: Manually override traffic signals for emergency situations.
* **Intersection Simulation**: Visual representation of traffic lights and their current states.
* **Map Integration**: Interactive map showing the intersection location.
* **Red-Light Violations**: Logs and displays incidents of red-light violations.
* **On-Call Officers**: List of traffic officers available for deployment.
* **Demo Tools**: Simulate violations, add officers, export reports, and reset the system.
* **System Logs**: View the latest 50 system events for monitoring and debugging.([GitHub][1], [BLOCKGENI][2], [GitHub][3], [GitHub][4])

---

## 📄 Documentation

For a detailed explanation of the system architecture, algorithms used, and future enhancements, please refer to the [Project Report](docs/Project_Report.pdf).

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

For any inquiries or feedback, please contact jawadsaad2004@hotmail.com, or hicham.w.saad@gmail.com

---

Feel free to customize the contact information and add any additional sections as needed. Let me know if you need assistance with anything else!

[1]: https://github.com/aaronseq12/AITrafficManagementSystem?utm_source=chatgpt.com "AI-based Traffic Management System that utilizes IoT and ... - GitHub"
[2]: https://blockgeni.com/ai-and-ml-based-integrated-traffic-management-system/?utm_source=chatgpt.com "AI and ML-Based Integrated Traffic Management System - BLOCKGENI"
[3]: https://github.com/Prit2341/Traffic-Management-Using-AI?utm_source=chatgpt.com "Prit2341/Traffic-Management-Using-AI - GitHub"
[4]: https://github.com/chahalbaljinder/RoadRanger-AI-Traffic-Optimization-System?utm_source=chatgpt.com "chahalbaljinder/RoadRanger-AI-Traffic-Optimization-System - GitHub"
