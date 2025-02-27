---

# 🚑 Traffic Accident Detection System with Emergency Alert 🚨

## Overview
On highways and road junctions at night, major accidents can occur without anyone nearby to call for help—especially if the injured person is unable to do so. This project aims to **automatically detect road accidents** using real-time surveillance camera feeds and **notify the nearest government hospital** immediately.

By integrating this system with **speed cameras** or **CCTV surveillance systems**, the hospital can remotely receive accident alerts along with the **time of the accident** and **camera location**. This system will enable faster emergency response and potentially save lives.

---

## 💻 Tech Stack & Tools Used 🔧
### Computer Vision  
- **YOLOv5** (Object Detection)  
- **OpenCV**
  
### Frontend  
- **HTML5 + CSS**  
- **Bootstrap**  
- **JavaScript**
  
### Backend  
- **Python**  
- **Flask** (Web Server & API)  
- **Socket Programming**  

---

## Installation & Setup Instructions ⚙️

### Prerequisites  
Make sure you have the following installed on your machine:  
- Python 3.8 or higher  
- Virtual Environment  
- pip (Python Package Installer)  

### Clone the Repository
```bash
git clone https://github.com/Shrey0808/TrafficAccidentDetector.git
cd TrafficAccidentDetector
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Download the YOLOv5 Pre-trained Model
Place your trained YOLOv5 model inside:
```bash
yolov5/runs/train/yolov5s_results2/weights/best.pt
```
Make sure the `best.pt` file is correctly downloaded.

---

### Run the System
1. Start the Hospital Dashboard:
```bash
python hospital_dashboard/run.py
```
Dashboard will be live at: **http://127.0.0.1:5000**

2. Start Accident Detection:
```bash
python accident_detector.py
```
Choose the input source:
- Webcam
- Video File

---

## Features 🔥
- Real-Time Accident Detection using **YOLOv5**
- Automatic **Alert System** with live timestamps
- Time and Location-Based Alerts
- Hospital Alert Dashboard
- Secure **Socket Communication**
- Cooldown Timer to avoid spam alerts
- Easy Web Interface

---

## Technical Workflow 🔄

### 1. Training the Model
- Trained on **Vehicle Accident Detection Dataset** from **Roboflow**
- YOLOv5 used for object detection
- Model detects vehicles involved in accidents with **85% confidence threshold**
- If accident-like motion is detected consistently for 30 frames, it is classified as an accident.

### 2. Accident Detection
- Reads video feed from webcam or video file
- Detects accidents using YOLOv5 model
- Sends **Time of Accident** and **Location** via **Socket Programming** to hospital server

### 3. Hospital Dashboard
- Flask web application
- Displays alerts with:
  - Time
  - Location

---

## How It Works 🔍
| Task               | Technology   |
|------------------|------------|
| Accident Detection | YOLOv5 |
| Image Processing  | OpenCV |
| Communication    | Socket Programming |
| Dashboard       | Flask + Bootstrap |

---

## Folder Structure
```bash
├── yolov5                   # YOLOv5 Model Folder
├── hospital_dashboard       # Flask App for Hospital Dashboard
│   ├── templates            # HTML Files
│   │    └── dashboard.html
│   └──run.py                # Flask Server
├── accident_detector.py     # Accident Detection System
├── requirements.txt         # Python Dependencies
└── README.md                # Project Documentation
```

---

## Future Improvements 💪
- Add **Email & SMS Alerts**
- Police Department Integration
- Live Streaming Access for Hospitals
- Severity Classification using Deep Learning
- Cloud-Based Deployment
- GPS Location Integration
  
---

## Conclusion ✅
This project offers an **automated emergency response system** that can significantly improve emergency services, reduce accident fatalities, and optimize hospital response times.

---

## Contributors 👨‍💻
- Shreyansh Sahay [(Shrey0808)](https://github.com/Shrey0808)
- Harsh Kumar [(hrsh-kmr)](https:://github.com/hrsh-kmr)

---

### GitHub Repository 🔗
👉 **[TrafficAccidentDetector](https://github.com/Shrey0808/TrafficAccidentDetector)** 

---
