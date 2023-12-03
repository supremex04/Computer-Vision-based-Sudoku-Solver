import cv2 as cv
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os

path = "./myData"
test_ratio = 0.2
validation_ratio = 0.2

listDir = os.listdir(path)
noOfClasses = len(listDir)

images = []
classNo = []


for i in range(0, noOfClasses):
    picList = os.listdir(path + "/" + str(i))
    #here image becomes the name of each image from the picList
    for image in picList:
        currentImage = cv.imread(path + "/"+ str(i) + "/"+ image)
        currentImage = cv.resize(currentImage, (30,30))
        images.append(currentImage)
        classNo.append(i)
    print(i, end = " ")
print(" ")
images = np.array(images)
classNo = np.array(classNo)
print("Original Size: " ,images.shape)


#splitting the data
x_train, x_test, y_train, y_test = train_test_split(images, classNo, test_size=test_ratio)
x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=validation_ratio)

# print(x_train.shape)
# print(x_test.shape)
# print(x_validation.shape)

noOfSamples = []

for x in range(0, noOfClasses):
    # np.where(y_train == x)[0] returns a list of all the indexes at which the class no. of y_train is 0 
    # ie. all the indexes where there is image of 0
    noOfSamples.append(len(np.where(y_train == x)[0]))
print(np.where(y_train == 0)[0])
print(noOfSamples)

plt.figure(figsize = (10,5))
plt.bar(range(0, noOfClasses), noOfSamples)
plt.title("No. of images for each class")
plt.xlabel("Class ID")
plt.ylabel("Number of images")
plt.show()

def preProcessing(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # to make the lighting distribute evenly in the image
    img = cv.equalizeHist(img)
    # in grayscale vale is from 0 to 255, we want 0 to 1
    img = img/255
    return img
# img = preProcessing((x_train[30]))
# img = cv.resize(img, (300,300))
# cv.imshow("Pre-processed image", img)
# cv.waitKey(0)

