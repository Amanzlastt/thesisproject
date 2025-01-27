import ultralytics
ultralytics.__version__

import sys
import os
import time
from datetime import datetime
sys.path.append(os.path.abspath("../src"))

try :
    from tracker import *
except ImportError :
    print('Import not done')




import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*

model=YOLO('yolov8n.pt')

class_list = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light']
tracker=Tracker()
count=0

cap=cv2.VideoCapture('video/traffic7.mp4')
down={}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3!= 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    a = results[0].boxes.data
    a = a.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    list = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c or 'truck' in c:
            list.append([x1, y1, x2, y2])
    bounding_box_id = tracker.update(list)

    for bounding_box in bounding_box_id:
        x3, y3, x4, y4, id = bounding_box
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2

        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)  # Draw bounding box
    
    text_color = (0, 0, 0)  # Black color for text
    yellow_color = (0, 255, 255)  # Yellow color for background
    red_color = (0, 0, 255)  # Red color for lines
    blue_color = (255, 0, 0)  # Blue color for lines
    offset = 6

    
    cv2.line(frame, (172, 398), (774, 398), red_color, 2)
    cv2.putText(frame, ('Red Line'), (172, 398), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    cv2.line(frame, (8, 468), (927, 468), blue_color, 2)
    cv2.putText(frame, ('Blue Line'), (8, 468), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    if 468<(cy+offset) and 398 > (cy-offset):
        down[id]=time.time()

    cv2.imshow("frames", frame)
    if cv2.waitKey(1) & 0xFF == 27:
    #if cv2.waitKey(0) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()