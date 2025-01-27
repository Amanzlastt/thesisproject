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


violation_folder = 'C:\\Users\\Aman\\Desktop\\thesisproject\\violators'

# Ensure the directory exists
if not os.path.exists(violation_folder):
    os.makedirs(violation_folder)

import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import*

model=YOLO('yolov8n.pt')

class_list = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light']
tracker=Tracker()
count=0

cap=cv2.VideoCapture('C:\\Users\\Aman\\Desktop\\thesisproject\\video\\highway (1).mp4')

down = {}
up = {}
counter_down = []
counter_up = []

red_line_y = 198
blue_line_y = 268
offset = 12

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 4!= 0:
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

        if red_line_y<(cy+offset) and red_line_y > (cy-offset):
           down[id]=time.time()   # current time when vehichle touch the first line
        if id in down:
          
           if blue_line_y<(cy+offset) and blue_line_y > (cy-offset):
             elapsed_time=time.time() - down[id]  # current time when vehicle touch the second line. Also we a re minusing the previous time ( current time of line 1)
             if counter_down.count(id)==0:
                counter_down.append(id)
                distance = 10 # meters 
                a_speed_ms = distance / elapsed_time
                a_speed_kh = a_speed_ms * 3.6  # this will give kilometers per hour for each vehicle. This is the condition for going downside
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                if a_speed_kh <= 30:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)  # Draw bounding box
                    cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                else :
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0,255), 2)  # Draw bounding box
                    cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    filename = datetime.now().strftime('%Y-%m-%d%H%M%S')
                    print(filename, type(filename))
                    cv2.imwrite(os.path.join(violation_folder, f'{filename}.jpg'), frame)
                    # cv2.imwrite(f'{filename}.jpg', frame)
                    print("printing")
        #####going UP blue line#####     
        if blue_line_y<(cy+offset) and blue_line_y > (cy-offset):
           up[id]=time.time()
        if id in up:

           if red_line_y<(cy+offset) and red_line_y > (cy-offset):
             elapsed1_time=time.time() - up[id]
             # formula of speed= distance/time 
             if counter_up.count(id)==0:
                counter_up.append(id)      
                distance1 = 10 # meters  (Distance between the 2 lines is 10 meters )
                a_speed_ms1 = distance1 / elapsed1_time
                a_speed_kh1 = a_speed_ms1 * 3.6
                cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                if a_speed_kh1 <= 30:
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)  # Draw bounding box
                    cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh1))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                else :
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0,255), 2)  # Draw bounding box
                    cv2.putText(frame,str(id),(x3,y3),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255),1)
                    cv2.putText(frame,str(int(a_speed_kh1))+'Km/h',(x4,y4 ),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),2)
                    filename = datetime.now().strftime('%Y-%m-%d%H%M%S')
                    cv2.imwrite(os.path.join(violation_folder, f'{filename}.jpg'), frame)
                    # cv2.imwrite(f'{filename}.jpg', frame)



    
    text_color = (0, 0, 0)  # Black color for text
    yellow_color = (0, 255, 255)  # Yellow color for background
    red_color = (0, 0, 255)  # Red color for lines
    blue_color = (255, 0, 0)  # Blue color for lines

    cv2.rectangle(frame, (0, 0), (250, 90), yellow_color, -1)

    cv2.line(frame, (172, 198), (774, 198), red_color, 2)
    cv2.putText(frame, ('Red Line'), (172, 198), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    cv2.line(frame, (8, 268), (927, 268), blue_color, 2)
    cv2.putText(frame, ('Blue Line'), (8, 268), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    cv2.putText(frame, ('Going Down - ' + str(len(counter_down))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(frame, ('Going Up - ' + str(len(counter_up))), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)


    cv2.imshow("frames", frame)
    if cv2.waitKey(1) & 0xFF == 27:
    #if cv2.waitKey(0) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


























# import pickle
# from ultralytics import YOLO
# from tracker import Tracker

# # Initialize model and tracker
# model = YOLO('yolov8n.pt')
# tracker = Tracker()

# # Save configurations
# configurations = {
#     "class_list": ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck'],
#     "red_line_y": 198,
#     "blue_line_y": 268,
#     "offset": 6
# }

# # Save to file
# with open("model_and_tracker.pkl", "wb") as f:
#     pickle.dump({"model": model, "tracker": tracker, "configurations": configurations}, f)

# # print("Model and tracker saved to model_and_tracker.pkl")
