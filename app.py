#################################
## Text2Type Web Interface
## ---------
## Runs the web interface for the Text2Type projects
## Collects form data and sends it to the IPP Server
## Run with 
##   python3 app.py
#########################
from flask import Flask, render_template, request
import requests

APP_PORT = 8080
IPP_SERVER_PORT = 5000
DEBUG = True

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/print', methods=['POST'])
def print_document():
    if 'file' not in request.files:
        app.logger.error("No file uploaded")
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        app.logger.error("No file selected")
        return "No selected file", 400

    try:
        resp = requests.post(f"http://localhost:{IPP_SERVER_PORT}", files=dict(file=request.files["file"]))
        if resp.status_code == 200:
            app.logger.info("Request sent to IPP Server successfully")
        else:
            app.logger.error(f"Request to IPP Server failed {resp.status_code}")
            return render_template("message.html", filename=file.filename, status=f"Request to IPP Server failed {resp.status_code}"), resp.status_code
    except Exception as e:
        app.logger.error(f"Failed to send request to IPP server: {e}")
        return render_template("message.html", filename=file.filename, status="Failed to send request to IPP server. Perhaps it is not running?"), 500

    return render_template("message.html", filename=file.filename, status="Successfully sent"), 200

if __name__ == '__main__':
    # run on 0.0.0.0 to make externally visable
    app.run("0.0.0.0", debug=DEBUG, port=APP_PORT)
