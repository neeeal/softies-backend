from flask import Flask, jsonify
import dotenv
import os
from tensorflow.keras.models import load_model
from flask_cors import CORS 

# Load the environment variables
dotenv.load_dotenv()

app = Flask(__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
CORS(app) 
model = None

############### RECOMMENDATION API ###############
def load_classifier():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    model = load_model('model/model.h5')

@app.route('/', methods=["GET"])
def index():
    if (model): 
        msg="Model was loaded successfully"
    else: 
        msg="Model was not loaded successfully"
    return jsonify({'msg':msg})

############### END OF RECOMMENDATION API ###############

if __name__ == '__main__':
    load_classifier()
    app.run(
        # 'localhost',
        port=os.getenv("PORT", default=8000)
        # debug=True
        )