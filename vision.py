import cv2 as cv
import numpy as np
from stackwindows import stackImages

path = "./Files/Images/test4.jpg"

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
cv.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

#largest contour
def largestContour(contours):
    maxArea = 0
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 100:
            perimeter = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02*perimeter,True)
            if (area > maxArea) and len(approx) == 4:
                largest = approx
                maxArea = area 
    return largest, maxArea

largest, maxArea = largestContour(contours)
#print("Approx;", largest)
#sort the points in largest = approx, which contains 4 corner points of the contour
def sortPoints(a):
    sum = []
    sortedList = [0,0,0,0]
    #get a list of sum of points
    for point in a:
        sum.append(point[0][0] + point[0][1])

    #farthest point
    sortedList[3] = [a[sum.index(max(sum)),0,0],a[sum.index(max(sum)),0,1]]
    #this will be 0,0 
    sortedList[0] = [a[sum.index(min(sum)),0,0],a[sum.index(min(sum)),0,1]]

    #for remaining two points
    for point in a:
        if (point[0][0]+ point[0][1]) != max(sum) and (point[0,0]+ point[0][1]) != min(sum):
            if (point[0,0] - point[0][1]) > 0:
                sortedList[1] = point[0].tolist()
            else:
                sortedList[2] = point[0].tolist()
    return sortedList

sortedList = sortPoints(largest)

#corner points of the bounding rectangle
x, y, w, h = cv.boundingRect(largest)
largestDetectImage = image.copy()
cv.circle(largestDetectImage, sortedList[0], 7, (255,0,0),cv.FILLED)
cv.circle(largestDetectImage, sortedList[1], 7, (255,0,0),cv.FILLED)
cv.circle(largestDetectImage, sortedList[2], 7, (255,0,0),cv.FILLED)
cv.circle(largestDetectImage, sortedList[3], 7, (255,0,0),cv.FILLED)

#wrap perspective
sourcePoints = np.float32(sortedList) 
destinationPoints = np.float32([[0,0],[w,0],[0,h],[w,h]])
matrix = cv.getPerspectiveTransform(sourcePoints,destinationPoints)
wrappedImage = cv.warpPerspective(image,matrix,(w,h))


blank = np.zeros((height, width,3), np.uint8)


imageList = [[image,blurredImage, threshold],[image_with_contours,largestDetectImage, wrappedImage]]
stackedImages =stackImages(0.6, imageList)


cv.imshow("window", stackedImages)
cv.waitKey(0)
cv.destroyAllWindows()