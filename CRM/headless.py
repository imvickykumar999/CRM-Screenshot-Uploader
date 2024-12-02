# import mss
# import mss.tools
# from datetime import datetime
# import os
# import requests
# import schedule
# import time

# # Configuration
# SAVE_DIR = os.path.join(os.getcwd(), "media/screenshots")
# UPLOAD_URL = "https://vickscrmss.pythonanywhere.com/api/upload_screenshot"
# os.makedirs(SAVE_DIR, exist_ok=True)

# def take_screenshot():
#     """Take a screenshot using mss."""
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filepath = os.path.join(SAVE_DIR, f"screenshot_{timestamp}.png")
#     with mss.mss() as sct:
#         monitor = sct.monitors[1]  # Capture the first monitor
#         sct_img = sct.grab(monitor)
#         mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
#     print(f"Screenshot saved to {filepath}")
#     return filepath

# def upload_screenshot(filepath):
#     """Upload the screenshot to the server."""
#     with open(filepath, "rb") as file:
#         files = {"file": file}
#         response = requests.post(UPLOAD_URL, files=files)
#     if response.status_code == 200:
#         print(f"Screenshot {filepath} uploaded successfully!")
#     else:
#         print(f"Failed to upload {filepath}: {response.status_code} - {response.text}")

# def job():
#     """Take and upload a screenshot."""
#     filepath = take_screenshot()
#     upload_screenshot(filepath)

# # Schedule the task every 10 seconds
# schedule.every(10).seconds.do(job)

# # Main loop to keep the scheduler running
# print("Starting the auto-screenshot uploader...")
# while True:
#     schedule.run_pending()
#     time.sleep(1)

###############################################################################

from pyvirtualdisplay import Display
from PIL import ImageGrab
import os
import time
import requests
from datetime import datetime
import schedule

# Configuration
SAVE_DIR = os.path.join(os.getcwd(), "media/screenshots")
UPLOAD_URL = "https://vickscrmss.pythonanywhere.com/api/upload_screenshot"
os.makedirs(SAVE_DIR, exist_ok=True)

# Setup virtual display
display = Display(visible=False, size=(1920, 1080))
display.start()

def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(SAVE_DIR, f"screenshot_{timestamp}.png")
    screenshot = ImageGrab.grab()
    screenshot.save(filepath, "PNG")
    print(f"Screenshot saved to {filepath}")
    return filepath

def upload_screenshot(filepath):
    with open(filepath, "rb") as file:
        files = {"file": file}
        response = requests.post(UPLOAD_URL, files=files)
    if response.status_code == 200:
        print(f"Screenshot {filepath} uploaded successfully!")
    else:
        print(f"Failed to upload {filepath}: {response.status_code} - {response.text}")

def job():
    filepath = take_screenshot()
    upload_screenshot(filepath)

schedule.every(10).seconds.do(job)

print("Starting the auto-screenshot uploader...")
while True:
    schedule.run_pending()
    time.sleep(1)
