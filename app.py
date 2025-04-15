#################################
## Text2Type Web Interface
## ---------
## Runs the web interface for the Text2Type projects
## Collects form data and sends it to the IPP Server
## Run with 
##   python3 app.py
#########################
from flask import Flask, render_template, request, jsonify
##import requests
from DriverCommunicator import BrailleDriverCommunicator

APP_PORT = 8080
IPP_SERVER_PORT = 5000
DEBUG = True
BRAILLE_DRIVER_PIPE = "/var/run/user/1000/text2touch_pipe"

DRIVER_IPC = True # set to True if using posix message queue for driver info

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
        with open(BRAILLE_DRIVER_PIPE, "w") as pipe:
            pipe.write(request.files["file"].read().decode())
    except OSError as e:
        app.logger.error(f"Failed to send request to IPP server: {e}")
        return render_template("message.html", filename=file.filename, status=f"Request to IPP Server failed {resp.status_code}"), resp.status_code

    return render_template("message.html", filename=file.filename, status="Successfully sent"), 200

messages: list[str] = []

@app.route('/admin')
def admin():
    return jsonify(messages)

if __name__ == '__main__':
    if DRIVER_IPC:
        # set up message queue
        driver_comm = BrailleDriverCommunicator()
        # set up callback to add messages to the list
        driver_comm.listen_status(messages.append)

    # run on 0.0.0.0 to make externally visable
    app.run("0.0.0.0", debug=DEBUG, port=APP_PORT)
