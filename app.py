from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    return 'This is my first API call!'

@app.route('/post', methods=["POST"])
def home():
    data = request.files['file']
    return jsonify({"status":"ok"})

if __name__ == '__main__':
     app.run(port:=8000)