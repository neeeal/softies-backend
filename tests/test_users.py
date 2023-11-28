from tensorflow.keras.models import load_model
from tensorflow import convert_to_tensor
import numpy as np
import cv2

def test_load_model():
    global model 
    model = load_model('model/model.h5')
    assert model

def test_classification_1():
    image = np.array(cv2.imread('assets/brownhopper.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 1	
def test_classification_2():
    image = np.array(cv2.imread('assets/false_smut.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 2 	
def test_classification_3():
    image = np.array(cv2.imread('assets/greenhopper.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 3	
def test_classification_4():
    image = np.array(cv2.imread('assets/healthy.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 4	
def test_classification_5():
    image = np.array(cv2.imread('assets/blast.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 5 	
def test_classification_6():
    image = np.array(cv2.imread('assets/Sheath_blight (39).png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 6 	
def test_classification_7():
    image = np.array(cv2.imread('assets/stemborer.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 7 	
def test_classification_8():
    image = np.array(cv2.imread('assets/tungro.jpg'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 8 	
def test_classification_9():
    image = np.array(cv2.imread('assets/yellowstemborer.png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 9	
def test_classification_10():
    image = np.array(cv2.imread('assets/BLB (14).png'))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (384,384))
    image = np.resize(image,(1,384,384,3))/255.
    classification = model(image)
    output = np.argmax(classification)+1
    assert output == 10 	
