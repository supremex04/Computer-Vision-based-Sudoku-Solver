import cv2 as cv
import numpy as np
from stackwindows import stackImages

path = "./pictures/test2.jpg"

height = 500
width = 500

image = cv.imread(path)
image = cv.resize(image, (width, height))

#pre-processing
grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blurredImage = cv.GaussianBlur(grayImage,(5,5),1)
threshold = cv.adaptiveThreshold(blurredImage, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 9,2)

#contour detection
contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
image_with_contours = image.copy()
cv.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

blank = np.zeros((height, width,3), np.uint8)


imageList = [[image,blurredImage, threshold],[threshold, image_with_contours,blank]]
stackedImages =stackImages(0.7, imageList)


cv.imshow("window", stackedImages)
cv.waitKey(0)
cv.destroyAllWindows()