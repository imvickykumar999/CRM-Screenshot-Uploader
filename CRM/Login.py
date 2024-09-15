import requests
import yaml
import getpass
import sqlite3
import hashlib

# Configuration
login_url = "http://127.0.0.1:5000/api/user/login"  # Localhost endpoint
db_path = 'user_credentials.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_credentials(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def login():
    count = 1
    while count < 5:
        username = input('Enter CRM username: ')
        password = getpass.getpass(prompt='Enter CRM password: ')

        hashed_password = hash_password(password)
        stored_password = get_user_credentials(username)

        if stored_password and hashed_password == stored_password:
            response = requests.post(login_url, data={'username': username, 'password': password})
            result = response.json()
            
            if response.status_code == 200 and result.get('status') == 1:
                token = result.get('token')
                print('Access granted')
                save_credentials(token)
                return
            else:
                print('Access denied by server. Try again.')
        else:
            print('Invalid username or password.')
        
        count += 1
        print(f'This is your attempt no. {count}')
    print("Failed to authenticate after multiple attempts.")

def save_credentials(token):
    config = {'token': token}
    with open("configlogin.yaml", 'w') as yamlfile:
        yaml.dump(config, yamlfile)
    print("Credentials saved to configlogin.yaml")

if __name__ == "__main__":
    login()
