import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

# current_directory = os.path.dirname(os.path.abspath(__file__))
# model_path = os.path.join(current_directory, 'model.h5')
# model = tf.keras.models.load_model(model_path)
# def test_load_model():
#     # Load the HDF5 data
#     f = h5py.File('model/model.h5', 'r')

#     # Extract model weights
#     weights = {}
#     for layer_name in f.keys():
#         if layer_name not in ['config', 'optimizer']:
#             weights[layer_name] = f[layer_name]

#     # Create a new model instance
#     global model
#     model = tf.keras.Sequential()

#     # Add layers and load weights
#     for layer_name, layer_weights in weights.items():
#         layer = tf.keras.layers.deserialize(layer_name, custom_objects={})
#         layer.set_weights(float(layer_weights))
#         model.add(layer)

#     # Compile the model
#     model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
#     assert model

# def test_load_custom_model():
#     # Open the HDF5 file in read-only mode
#     with h5py.File('model/model.h5', 'r') as file:
#         # Check if the file contains the required model attributes
#         if 'model_weights' not in file or 'model_config' not in file:
#             raise ValueError("Invalid HDF5 file. Missing model weights or configuration.")

#         # Load the model configuration
#         model_config = file['model_config'].value
#         model_config = tf.keras.utils.json_utils.decode(model_config)

#         # Create an empty model
#         model = tf.keras.models.model_from_config(model_config)

#         # Load the model weights
#         model_weights_group = file['model_weights']
#         model.load_weights_from_hdf5_group(model_weights_group)
#     assert model

def test_load_model():
    model = load_model('model.h5')
    assert model


def test_classification_1():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/brownhopper.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 1	
def test_classification_2():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/false_smut.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 2 	
def test_classification_3():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/greenhopper.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 3	
def test_classification_4():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/healthy.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 4	
def test_classification_5():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/blast.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 5 	
def test_classification_6():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/Sheath_blight (39).png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 6 	
def test_classification_7():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/stemborer.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 7 	
def test_classification_8():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/tungro.jpg'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 8 	
def test_classification_9():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/yellowstemborer.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 9	
def test_classification_10():
    model = load_model('model.h5')
    image = np.array(cv2.imread('assets/BLB (14).png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 10 	
