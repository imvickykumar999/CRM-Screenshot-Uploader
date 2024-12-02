import os
import time
import requests
from PIL import ImageGrab
from datetime import datetime
import schedule

# Configuration
SAVE_DIR = os.path.join(os.getcwd(), "media/screenshots")  # Ensure absolute path
UPLOAD_URL = "http://192.168.1.18:5000/api/upload_screenshot"
# UPLOAD_URL = "https://vickscrmss.pythonanywhere.com/api/upload_screenshot" 

# Ensure the directory for saving screenshots exists
os.makedirs(SAVE_DIR, exist_ok=True)

def take_screenshot():
    """Take a screenshot and save it locally."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SAVE_DIR, f"screenshot_{timestamp}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(filepath, "PNG")
    print(f"Screenshot saved to {filepath}")
    return filepath

def upload_screenshot(filepath):
    """Upload the screenshot to the server."""
    with open(filepath, "rb") as file:
        files = {"file": file}
        response = requests.post(UPLOAD_URL, files=files)

    if response.status_code == 200:
        print(f"Screenshot {filepath} uploaded successfully!")
    else:
        print(f"Failed to upload {filepath}: {response.status_code} - {response.text}")

def job():
    """Take and upload a screenshot."""
    filepath = take_screenshot()
    upload_screenshot(filepath)

# Schedule the task every 10 seconds
schedule.every(10).seconds.do(job)

# Main loop to keep the scheduler running
print("Starting the auto-screenshot uploader...")
while True:
    schedule.run_pending()
    time.sleep(1)

