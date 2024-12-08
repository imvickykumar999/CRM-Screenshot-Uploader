from flask import Flask, render_template
import os

print(__name__, __file__)
# Specify the template folder to the current directory
app = Flask(__name__, template_folder=os.path.dirname(__file__))

@app.route('/')
def hello_world():
    # Flask will now look for index.html in the same folder as app.py
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
