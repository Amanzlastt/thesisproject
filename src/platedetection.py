import cv2
import os

# Open the video file
video_path = 'C:\\Users\\Aman\\Desktop\\thesisproject\\video\\plate1.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a directory to store frames
output_dir = 'extracted_frames'
os.makedirs(output_dir, exist_ok=True)

# Frame extraction parameters
frame_count = 0
frame_interval = 30  # Extract one frame every 30 frames

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frames are left

    # Save the frames at the specified interval
    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_dir, f'frame_{frame_count}.jpg')
        cv2.imwrite(frame_filename, frame)
        print(f'Saved: {frame_filename}')

    frame_count += 1

# Release the video capture object
cap.release()
cv2.destroyAllWindows()