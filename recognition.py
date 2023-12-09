import numpy as np
import cv2 as cv
from keras.models import load_model


def initializeModel():
    model = load_model("./Files/Model/model.h5")
    return model