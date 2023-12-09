import numpy as np
import cv2 as cv
from keras.models import load_model

def initializeModel():
    model = load_model("./Files/Model/model.h5")
    return model

def getPrediction(boxes, model):
    result = []
    count = 0
    for image in boxes:
        img = np.asarray(image)
        img = img[4:img.shape[0] - 4, 4:img.shape[1] -4]
        img = cv.resize(img, (28,28))
        img = img/255
        img = img.reshape(1,28,28,1)
        predictions = model.predict(img)
        classIndex = np.argmax(predictions, axis =-1)
        probabilityValue = np.amax(predictions)
        if count ==1:
            print(classIndex, probabilityValue)
        count +=1
        #saving the result
        if probabilityValue> 0.7:
            result.append(classIndex[0])

        else:
            result.append(0)
    return result

def oranizer(result):
    revised = []
    temp = []
    for i in range(len(result)):
        if (i%9 == 0 and i != 0):
            revised.append(temp)
            temp = []
        temp.append(result[i])
    revised.append(temp)
    return revised

    