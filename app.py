from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os

ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv', 'jpeg', 'jpg'])
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Downloads'))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
# cors = CORS(app)
app.config['CORS_HEADER'] = 'application/json'
# openai.api_key = 'your_api_key_here'


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# API to upload file
@app.route('/upload', methods=['POST', 'GET'])
def fileUpload():
    if request.method == 'POST':
        file = request.files.getlist('files')
        filename = ""
        print(request.files, "....")
        for f in file:
            print(f.filename)
            filename = secure_filename(f.filename)
            print(allowedFile(filename))
            if allowedFile(filename):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return jsonify({'message': 'File type not allowed'}), 400
        return jsonify({"name": filename, "status": "success"})
    else:
        return jsonify({"status": "Upload API GET Request Running"})




@app.route('/prompt', methods=['POST', 'GET'])
def prompt():
    if request.method == 'POST':
        return jsonify({"status": 200, "message": "Prompt API POST Request Running"})
    #   prompt = request.json.get('prompt')
    #   result = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=prompt,
    #     max_tokens=100
    # )
    # return jsonify({"result": result['choices'][0]['text']})
    else:
        return jsonify({'status': 200, "message": "Prompt API GET Request Running"})
