from flask import Flask, request, jsonify, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'media')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.route('/upload_screenshot', methods=['POST'])
def upload_screenshot():
    """Handle screenshot upload."""
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully", "url": f"/media/{file.filename}"})

@app.route('/', methods=['GET'])
def list_screenshots():
    """Fetch and display uploaded screenshots."""
    screenshots = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(('jpg', 'jpeg', 'png')):
            screenshots.append({
                'url': f"/media/{filename}"
            })
    screenshots.reverse()
    return jsonify(screenshots)

@app.route('/media/<filename>')
def serve_screenshot(filename):
    """Serve uploaded screenshot files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

