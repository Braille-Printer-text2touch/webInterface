from flask import Flask, render_template, request
import os

app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         user_input = request.form.get('user_input')
#         # Process the input as needed
#         return f"You entered: {user_input}"  # Displays the input on the page
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=80)  # Runs the app on port 80
@app.route('/')
def index():
    app.logger.info("Index route is called")
    return render_template('index.html')
    

@app.route('/print', methods=['POST'])
def print_document():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = f'/tmp/{file.filename}'
    file.save(file_path)

    try:
        # Send file to CUPS for printing
        os.system(f'lp {file_path}')
    except Exception as e:
        return f"Error during printing: {str(e)}", 500

    # Optionally clean up the file after printing
    os.remove(file_path)

    return f"File '{file.filename}' successfully printed.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)