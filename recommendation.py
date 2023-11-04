from tensorflow.keras.saving import load_model
import cv2
import numpy as np

## Testing impors for model
from tensorflow.keras.applications.efficientnet_v2 import EfficientNetV2L
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential

from flask import Flask, render_template, redirect, request, jsonify, session
# from flask_session import Session
from pymysql import connect
from pymysql.cursors import re, DictCursor
import hashlib

app = Flask(__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
app.secret_key = 'skanin is the best'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# session = Session(app)
# print(session)

image_size = (224)
channels = 3

# Connect to the database
connection = connect(host='localhost',
                             user='root',
                            #  password='passwd',
                             database='skanin_db',
                            #  charset='utf8mb4',
                             cursorclass=DictCursor)

def initModel():
    ## Model initialization function
    # IMG_SHAPE = (image_size,image_size) + (channels,) ## RGB=3
    tf_model = load_model('assets//efficientnetv2-s-imagenet.h5')
    return tf_model

def preprocessData(data):
    ## Main Preprocessing function for input images 
    processed_data = cv2.resize(data.file,(image_size,image_size),cv2.INTER_LINEAR)
    processed_data = cv2.cvtColor(processed_data, cv2.COLOR_BGR2RGB)
    return processed_data

@app.route('/skan', methods=["POST"])
def skan():
    ## Prediction route accepting images and outputs prediction of A.I.
    data = request.files['file']
    processed_data = preprocessData(data)
    result = np.argmax(model.predict(processed_data))
    return jsonify({"result":result})

@app.route('/recommendation', methods=["GET"])
def recommendation():
    ## Recommendation route based on result
    stress_id = int(request.args["result"])
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * from rice_stress WHERE `stress_id` = {stress_id}")
        stress = cursor.fetchone()
    stress_name = stress['stress_name']
    stress_type = stress['stress_type']
    stress_level = stress['stress_level']
    description = stress['description']
    description_src = stress['description_src']
    recommendation = stress['recommendation']
    recommendation_src = stress['recommendation_src']
    msg = 'Successfully retrieved recommendation'
    return jsonify({'msg':msg, 'stress_name':stress_name, stress_type:'stress_type',
                    'stress_level':stress_level, 'description':description, 'description_src':description_src,
                    'recommendations':recommendation, 'recommendation_src':recommendation_src})

if __name__ == '__main__':
    model = initModel()
    print('running')
    app.run(port=5000)