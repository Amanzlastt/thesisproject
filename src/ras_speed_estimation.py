import cv2
import time
import pandas as pd 
from datetime import datetime
from ultralytics import YOLO
from tracker import Tracker 
import requests

model = YOLO('yolov8.pt')
class_list = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck']
tracker = Tracker()
speed_limit_km

def send_frame_to_server(frame, filename):
    print('Sending frame to server ...')
    url = "http://192.168.78.1:5000/upload"
    _, img_encoder = cv2.imencode('.jpg', frame)
    response = requests.post(
        url,
        files={"image": (f"{filename}.jpg", img_encoder.tobytes(), 'image/jpeg')}
    )
    print(f"Server response: {response.status_code} - {response.text}")

cap = cv2.VideoCapture('/home/raspberrypi/video.mp4')

count =  0
down, up = {}, {}
counter_down, counter_up = [], []
red_line_y = 198
blue_line_y = 268
offset = 12
speedlimit_kmph = 3
line_distance_m = 10
print("Video capture has started")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 4 !=0:
        continue
    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    detections = results[0].boxes.data.cpu().numpy()
    df = pd.DataFrame(detections).astype("float")

    vehicles = []
    for _, row in df.iterrows():
        x1, y1, x2, y2, _, cls_id = map(int, row[:6])
        label = class_list[cls_id] if cls_id < len(class_list) else ""
        if "car" in label or 'truck' in label:
            vehicles.append([x1, y1, x2, y2])
    tracked = tracker.update(vehicles)
    for bbox in tracked:
        x3, y3, x4, y4, obj_id = bbox
        cx = (x3 +x4) // 2
        cy = (y3+ y4)  // 2

        if red_line_y - offset < cy_red_line_y + offset:
            down[obj_id] = time.time()
        
        if obj_id in down and blue_line_y - offset < cy < blue_line_y + offset:
            elapsed = time.time() - down[obj_id]
            if obj_id not in counter_down:
                counter_down.append(obj_id)
                speed = (line_distance_m /elapsed) * 3.6
            if speed > speed_limit_kmph:
                filename = datetime.now().strftime('%Y%m%d%H%M%S')
                cropped_vehicle = frame.copy()
                if cropped_vehicle.size > 0:
                    cv2.rectangle(cropped_vehicle, (x3, y3), (x4, y4), (0,0, 255), 2)
                    cv2.putText(cropped_vehicle, f"{int(speed)} Km/h", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0, 255), 2)
                    send_frame_to_server(cropped_vehicle, filename)
    
cap.release()



