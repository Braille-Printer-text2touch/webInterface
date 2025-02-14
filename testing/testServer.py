from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def submit():
    app.logger.debug(f"File data: {request.files}")
    with open("./temp", "wb") as f:
        request.files["file"].save(f)
    return "File accepted", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
