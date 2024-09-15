import requests
import yaml
import getpass
import os
import time
import pyautogui as ImageGrab
from datetime import datetime
import jwt

# Configuration
update_interval_screenshot = 10  # time in seconds

# Get the current working directory dynamically
directory = os.path.join(os.getcwd(), "screenshots")
api_url = "https://vickscrm.pythonanywhere.com/api/user/upload_screenshot"  # Adjust URL as needed

# Load credentials and token
with open("configlogin.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    status = int(data['status'])
    token = data['token']
    print("Read successful")

def take_screenshot():
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    image_name = f"{getpass.getuser()}_{timestamp}.png"
    filepath = os.path.join(directory, image_name)
    
    screenshot = ImageGrab.screenshot()
    screenshot.save(filepath)
    print(f"Screenshot saved: {filepath}")
    return filepath

def upload_then_delete_local_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            headers = {"Authorization": f"Bearer {token}"}
            files = {'file': file}
            response = requests.post(api_url, headers=headers, files=files)
            
            if response.status_code == 200:
                print(f"File uploaded successfully: {filepath}")
            else:
                print(f"Failed to upload file: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error during file upload: {str(e)}")
    finally:
        # Ensure the file is deleted after attempting upload
        try:
            os.remove(filepath)
            print(f"Local file deleted: {filepath}")
        except Exception as e:
            print(f"Error deleting file: {str(e)}")

def main():
    if not os.path.exists(directory):
        os.makedirs(directory)
    while True:
        screenshot_path = take_screenshot()
        upload_then_delete_local_file(screenshot_path)
        time.sleep(update_interval_screenshot)

if __name__ == "__main__":
    main()
