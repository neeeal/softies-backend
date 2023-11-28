import tensorflow as tf
import numpy as np
import cv2
import gdown
model=None

def test_load_model():
    global model
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
    model.compile(optimizer=tf.keras.optimizers.legacy.RMSprop(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
    url = 'https://drive.google.com/drive/folders/1ptqlr_T0XRs88FAoucKSf7pxcEixRZ9O'
    gdown.download_folder(url, quiet=True, use_cookies=False)
    model.load_weights(filepath='model_weights/')
    for layer in model.layers:
        layer.trainable = False
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
