import sqlite3
import getpass
import hashlib

# Database setup
db_path = 'user_credentials.db'

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    create_table()
    username = input('Enter new username: ')
    password = getpass.getpass(prompt='Enter new password: ')

    hashed_password = hash_password(password)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print('User registered successfully')
    except sqlite3.IntegrityError:
        print('Username already exists')
    finally:
        conn.close()

if __name__ == "__main__":
    register()
