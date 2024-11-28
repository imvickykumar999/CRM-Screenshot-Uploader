import os
import time
import requests
from PIL import ImageGrab
from datetime import datetime
import schedule

basepath = 'https://vickscrm.pythonanywhere.com'
# basepath = 'http://localhost:5000'

# Configuration
SAVE_DIR = "screenshots"
LOGIN_URL = f"{basepath}/api/user/login"
UPLOAD_URL = f"{basepath}/api/user/upload_screenshot"

USERNAME = "vicky"
PASSWORD = "kumar"
TOKEN = None  # Placeholder for the token

# Ensure the directory for saving screenshots exists
os.makedirs(SAVE_DIR, exist_ok=True)

def get_token():
    """Fetch a new token."""
    global TOKEN
    response = requests.post(LOGIN_URL, data={"username": USERNAME, "password": PASSWORD})
    if response.status_code == 200:
        TOKEN = response.json().get("token")
        print("Token fetched successfully!")
    else:
        print(f"Failed to login: {response.status_code} - {response.text}")
        TOKEN = None

def take_screenshot():
    """Take a screenshot and save it locally."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SAVE_DIR, f"screenshot_{timestamp}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(filepath, "PNG")
    print(f"Screenshot saved to {filepath}")
    return filepath

def upload_screenshot(filepath):
    """Upload the screenshot to the API."""
    if not TOKEN:
        print("No valid token. Skipping upload.")
        return

    with open(filepath, "rb") as file:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        files = {"file": file}
        response = requests.post(UPLOAD_URL, headers=headers, files=files)

    if response.status_code == 200:
        print(f"Screenshot {filepath} uploaded successfully!")
        try:
            os.remove(filepath)  # Delete the screenshot after successful upload
            print(f"Screenshot {filepath} deleted successfully.")
        except Exception as e:
            print(f"Failed to delete {filepath}: {e}")
    elif response.status_code == 401:
        print(f"Token expired or invalid. Fetching a new token...")
        get_token()  # Refresh token
    else:
        print(f"Failed to upload {filepath}: {response.status_code} - {response.text}")

def job():
    """Take and upload a screenshot."""
    filepath = take_screenshot()
    upload_screenshot(filepath)

# Get initial token
get_token()

# Schedule the task every 10 seconds
schedule.every(10).seconds.do(job)

# Main loop to keep the scheduler running
print("Starting the auto-screenshot uploader...")
while True:
    schedule.run_pending()
    time.sleep(1)
