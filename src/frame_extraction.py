import cv2
import os

# === CONFIGURATION ===
video_path = "C:\\Users\\Aman\\Desktop\\thesisproject\\video\\video_2.mp4"  # Update with your video path
output_folder = "C:/Users/Aman/Desktop/thesisproject/extracted_frames3"  # Folder to save frames
frame_interval = 15  # Extract every Nth frame (e.g., 30 = 1 frame per second for 30fps video)

# === CREATE OUTPUT FOLDER IF NOT EXISTS ===
os.makedirs(output_folder, exist_ok=True)

# === OPEN VIDEO FILE ===
cap = cv2.VideoCapture(video_path)
frame_count = 0
saved_count = 0

if not cap.isOpened():
    print("❌ Error opening video file.")
    exit()

# === FRAME EXTRACTION LOOP ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_interval == 0:
        filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1

    frame_count += 1

cap.release()
print(f"✅ Done. Extracted {saved_count} frames to: {output_folder}")
