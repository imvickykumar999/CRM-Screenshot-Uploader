import os
import time
import requests
import cv2
from datetime import datetime
import schedule

SAVE_DIR = os.path.join(os.getcwd(), "media")  # Ensure absolute path
UPLOAD_URL = "http://127.0.0.1:5000/upload_screenshot"
# UPLOAD_URL = "https://crmss.pythonanywhere.com/upload_screenshot" 
os.makedirs(SAVE_DIR, exist_ok=True)

def take_camera_photo():
    """Take a photo using the camera and save it locally."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SAVE_DIR, f"photo_{timestamp}.png")
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is the default camera index
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return None
    
    # Capture a single frame
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filepath, frame)
        print(f"Photo saved to {filepath}")
    else:
        print("Error: Could not capture photo.")
        filepath = None
    
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()
    
    return filepath

def upload_screenshot(filepath):
    """Upload the photo to the server."""
    if filepath is None:
        print("No photo to upload.")
        return
    
    with open(filepath, "rb") as file:
        files = {"file": file}
        response = requests.post(UPLOAD_URL, files=files)
    if response.status_code == 200:
        print(f"Photo {filepath} uploaded successfully!")
    else:
        print(f"Failed to upload {filepath}: {response.status_code} - {response.text}")

def job():
    """Take and upload a camera photo."""
    filepath = take_camera_photo()
    upload_screenshot(filepath)

schedule.every(10).seconds.do(job)
print("Starting the auto-camera photo uploader...")
while True:
    schedule.run_pending()
    time.sleep(1)
