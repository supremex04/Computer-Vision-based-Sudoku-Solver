import cv2 as cv
import numpy as np
from stackwindows import stackImages

path = "./pictures/test4.jpg"

height = 500
width = 500

image = cv.imread(path)
image = cv.resize(image, (width, height))

#pre-processing
grayImage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
blurredImage = cv.GaussianBlur(grayImage,(5,5),1)
threshold = cv.adaptiveThreshold(blurredImage, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 15,7)

#contour detection
contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
image_with_contours = image.copy()
#cv.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

#largest contour
def largestContour(contours):
    maxArea = 0
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 100:
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02*perimeter,True)
            if (area > maxArea) and len(approx) == 4:
                largest = contour
                maxArea = area 
    return largest, maxArea

largest, maxArea = largestContour(contours)
perimeter = cv.arcLength(largest, True)
approx = cv.approxPolyDP(largest, 0.02*perimeter,True)
print("Approx;", type(approx))
cv.drawContours(image_with_contours, largest, -1, (0, 255, 0), 5)


#corner points of the bounding rectangle
x, y, w, h = cv.boundingRect(largest)
#sourcePoints = np.float32([x,y],[]) 
largestDetectImage = image.copy()
cv.circle(largestDetectImage, (125, 139), 7, (0,0,255),cv.FILLED)
cv.circle(largestDetectImage, (369, 144), 7, (0,0,255),cv.FILLED)
cv.circle(largestDetectImage, (132, 457), 7, (0,0,255),cv.FILLED)
cv.circle(largestDetectImage, (376, 427), 7, (0,0,255),cv.FILLED)



blank = np.zeros((height, width,3), np.uint8)


imageList = [[image,blurredImage, threshold],[image_with_contours,largestDetectImage, blank]]
stackedImages =stackImages(0.6, imageList)


cv.imshow("window", stackedImages)
cv.waitKey(0)
cv.destroyAllWindows()