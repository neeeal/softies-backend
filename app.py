from flask import Flask, request, jsonify
from tensorflow.keras.saving import load_model
import cv2
import numpy as np

## Testing impors for model
from tensorflow.keras.applications.efficientnet_v2 import EfficientNetV2L
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential

app = Flask(__name__)
image_size = 480
## fake data lists
classes = [i for i in range(0,1000)]
actions = ['a'*i for i in range(0,1000)]

def initModel(image_size=image_size):
    ## Model initialization function
    IMG_SHAPE = (image_size,image_size) + (3,) ## RGB=3
    tf_model = EfficientNetV2L(input_shape=IMG_SHAPE,
                                include_top=True,
                                weights='imagenet')
    return tf_model

def preprocessData(data, image_size=image_size):
    ## Main Preprocessing function for input images 
    processed_data = cv2.resize(data.file,(image_size,image_size),cv2.INTER_LINEAR)
    processed_data = cv2.cvtColor(processed_data, cv2.COLOR_BGR2RGB)
    return processed_data

@app.route('/landing', methods=["GET"])
def landing():
    return 'This is my first API call!'

@app.route('/prediction', methods=["POST"])
def prediction():
    ## Prediction route accepting images and outputs prediction of A.I.
    data = request.files['file']
    processed_data = preprocessData(data)
    result = np.argmax(model.predict(processed_data))
    class_ = classes[result]
    return jsonify({"result":result, "class":class_})

@app.route('/recommendation', methods=["GET"])
def recommendation():
    ## Recommendation route based on result
    result, class_ = request.args["result","class"]
    if int(result) >= 500:
        type_ = 'biotic'
    else:
        type_ = 'abiotic'
    recommended_action = actions[int(class_)]
    return jsonify({"type":type_, "recommended_action":recommended_action})

if __name__ == '__main__':
    model = initModel()
    app.run(port=8000)