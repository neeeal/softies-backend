from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, redirect, request, jsonify, session, Blueprint
from pymysql import connect
from pymysql.cursors import re, DictCursor
import numpy as np
import cv2
from PIL import Image
import dotenv
import os
import tensorflow as tf
# Load the environment variables
dotenv.load_dotenv()

recommendation_bp = Blueprint('recommendation',__name__)
# Change this to your secret key (it can be anything, it's for extra protection)
recommendation_bp.secret_key = os.getenv("SECRET_KEY")
# recommendation_bp.config["SESSION_PERMANENT"] = False
# recommendation_bp.config["SESSION_TYPE"] = "filesystem"

image_size = (224)
channels = 3

# Connect to the database
connection = connect(host=os.getenv("DATABASE_URL"),
                    user=os.getenv("USER"),
                    password=os.getenv("PASSWORD"),
                    database=os.getenv("DATABASE_NAME"),
                    cursorclass=DictCursor,
                    # port=int(os.getenv("DATABASE_PORT"))
                    )

# Model initialization
model=None
# Define the function to handle the KerasLayer when loading the model
def load_m():
    target_size = (384, 384)
    efficientnetv2 = tf.keras.applications.efficientnet_v2.EfficientNetV2S(
                    include_top=False,
                    weights='imagenet',
                    input_tensor=None,
                    input_shape=target_size+(3,),
                    pooling='avg',
                    # classes=1000,
                    # classifier_activation='softmax',
                )
    # Create a new model on top of EfficientNetV2
    model = tf.keras.Sequential()
    # model.add(tf.keras.layers.Input(target_size+(3,)))
    model.add(efficientnetv2)
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.BatchNormalization())
    # model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(1024, activation = 'relu'))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(1024, activation = 'relu'))
    # model.add(tf.keras.layers.Dropout(0.5))
    # model.add(tf.keras.layers.Dense(1024, activation = 'relu'))
    # model.add(tf.keras.layers.Dropout(0.5))
    # model.add(tf.keras.layers.Dense(1024, activation = 'relu'))
    # model.add(tf.keras.layers.Dropout(0.5))
    # model.add(tf.keras.layers.Dense(512, activation = 'relu'))
    # model.add( tf.keras.layers.Dense(64, activation = 'softmax'))
    # model.add( tf.keras.layers.Dense(32, activation = 'softmax'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))
    model.compile(optimizer=tf.keras.optimizers.RMSprop(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def preprocessData(data, image_size = 384):
    ## Main Preprocessing function for input images 
    img = cv2.resize(data,(image_size,image_size))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array *= 1./255
    return img_array

@recommendation_bp.route('/skan', methods=["POST"])
def skan():
    if request.method == 'POST' and 'image' in request.files:
        ## Retrieving user_id
        user_id = session.get('user_id')
        print(user_id)
        ## Prediction route accepting images and outputs prediction of A.I.
        ## Read Image from input and convert to CV2
        image = request.files['image']
        image_name=image.filename
        ## Checking file name if jpg jpeg or png
        if image_name.split('.')[-1] not in ["jpeg", "png", "jpg"]:
            msg = "Invalid file type. Submit only .jpg, .png, or .jpeg files."
            return jsonify({"msg":msg})
        pil_image = Image.open(image.stream).convert('RGB').resize((300, 300))
        data = np.array(pil_image)
        

        ## Image for saving
        rice_image = data.tobytes()

        ## Model prediction
        global model
        if model == None:
            model = load_m()#load_model('model_text.h5')
        # data = preprocessData(data)
        # result = np.argmax(model(data))+1
        # print(result)
        # print("INSERT HERE")
        result = '3'
            ## End of prediction

        ## Getting Recommendation using output from model
        stress_id = int(result)
        connection.ping(reconnect=True)
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

        ## Creating history entry for transaction
        with connection.cursor() as cursor:
            # print("working")
            sql = "INSERT INTO `history` (`user_id`, `stress_id`, `rice_image`, `image_name`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, stress_id, rice_image, image_name))
        connection.commit()
        
        return jsonify({'msg':msg, 'stress_name':stress_name, stress_type:'stress_type',
                        'stress_level':stress_level, 'description':description, 'description_src':description_src,
                        'recommendations':recommendation, 'recommendation_src':recommendation_src})
    msg = 'Invalid request'
    return jsonify({'msg':msg})


# if __name__ == '__main__':
#     recommendation_bp.run('localhost',port=8000, debug=True)