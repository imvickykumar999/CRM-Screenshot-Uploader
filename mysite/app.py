from flask import Flask, request, jsonify, render_template
import jwt
import datetime
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Database setup
db_path = 'user_credentials.db'

def init_db():
    """Initialize the database."""
    if not os.path.exists(db_path):
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

init_db()

def hash_password(password):
    """Hash a password using SHA-256."""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_password(username):
    """Fetch the hashed password for a given username."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_user(username, hashed_password):
    """Save a new user to the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

@app.route('/ss')
def index():
    return render_template('index.html')

@app.route('/api/user/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    hashed_password = hash_password(password)
    if save_user(username, hashed_password):
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "User already exists"}), 400

@app.route('/api/user/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    hashed_password = hash_password(password)
    stored_password = get_user_password(username)

    if stored_password and hashed_password == stored_password:
        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/api/user/upload_screenshot', methods=['POST'])
def upload_screenshot():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401

    # Remove 'Bearer ' prefix if it exists
    if token.startswith('Bearer '):
        token = token[len('Bearer '):]

    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        username = data['username']
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token is invalid"}), 401

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    file.save(f"static/images/{file.filename}")
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/ss_api/', methods=['GET'])
def get_screenshots():
    """Fetch all uploaded screenshots and return as JSON."""
    screenshots_folder = 'static/images/'
    screenshots = []
    
    # List all files in the screenshots folder
    for filename in os.listdir(screenshots_folder):
        if filename.endswith(('jpg', 'jpeg', 'png', 'gif')):
            screenshots.append({
                'filename': filename,
                'url': f'/static/images/{filename}'
            })
    
    return jsonify(screenshots)

@app.route('/')
def screenshots():
    return render_template('screenshots.html')

if __name__ == '__main__':
    app.run(debug=True)
