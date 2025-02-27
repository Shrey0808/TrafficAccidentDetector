import sys
sys.path.append('./yolov5')  # Add YOLOv5 folder to path

import os
import cv2
import torch
import time
from models.experimental import attempt_load
from utils.general import non_max_suppression, check_img_size
from utils.torch_utils import select_device
import numpy as np

# Global Variables
accident_frames = 0
consecutive_accident_frames = 0
frame_count = 0
threshold = 30
cooldown = False
cooldown_start = 0
cooldown_time = 15 * 60  # 15 minutes in seconds

def load_model(weights):
    device = select_device('')
    model = torch.load(weights, map_location=device)  # Load weights
    model = model['model'].float().fuse().eval()      # Convert model to FP32 and set to evaluation mode
    return model, device

def detect_accident(frame, model, device, img_size=640):
    global accident_frames, consecutive_accident_frames
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (img_size, img_size))
    img = np.transpose(img, (2, 0, 1))
    img = torch.from_numpy(img).float().div(255.0).unsqueeze(0).to(device)

    # YOLO Detection
    with torch.no_grad():
        pred = model(img)[0]
        pred = non_max_suppression(pred, 0.85, 0.45)

    detected = False
    for det in pred:
        if len(det):
            accident_frames += 1
            consecutive_accident_frames += 1
            detected = True
            if not cooldown:
                print(f"🚨 Accident Detected at Frame {frame_count}")

    # Reset consecutive count if no accident detected
    if not detected:
        consecutive_accident_frames = 0

def accident_detection(source):
    global frame_count, accident_frames, cooldown, cooldown_start, consecutive_accident_frames

    model, device = load_model("yolov5/runs/train/yolov5s_results2/weights/best.pt")

    if source == "0":
        source = 0
        print("Webcam selected...")

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Cannot open video source")
        return

    print("Starting Real-Time Accident Detection...\nPress 'q' to stop")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        detect_accident(frame, model, device)

        # Cooldown logic based on consecutive frames
        if consecutive_accident_frames >= threshold and not cooldown:
            print("\n🚑 ALERT: Severe Accident Detected! Sending Alert to Hospital...\n")
            cooldown = True
            cooldown_start = time.time()
            consecutive_accident_frames = 0  # Reset consecutive counter after alert
        
        if cooldown:
            elapsed = time.time() - cooldown_start
            if elapsed >= cooldown_time:
                print("\nCooldown Period Ended!\n")
                cooldown = False
                accident_frames = 0

        # Display video without bounding boxes
        cv2.imshow("Accident Detection", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\nTotal Frames Processed: {frame_count}")
    print(f"Accident Frames Detected: {accident_frames}")
    if accident_frames > threshold:
        print("✅ Hospital Alert Sent!")
    else:
        print("No Severe Accident Detected.")

# User Interface
print("=" * 40)
print("Accident Detection System")
print("=" * 40)
print("\nSelect input source:")
print("1. Webcam (0)")
print("2. Video file")

choice = input("Enter choice (1/2): ")

if choice == "1":
    accident_detection("0")
elif choice == "2":
    file_path = input("Enter video file path: ")
    if os.path.exists(file_path):
        accident_detection(file_path)
    else:
        print("Invalid File Path!")
else:
    print("Invalid Choice!")
