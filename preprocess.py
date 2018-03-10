import cv2 as cv
import numpy as np
import sys

def cv_close(img, kernel, depth = 1):
    return cv.erode(cv.dilate(img, kernel, depth), kernel, depth)

def cv_open(img, kernel, depth = 1):
    return cv.dilate(cv.erode(img, kernel, depth), kernel, depth)

def cv_invert(img):
    return (255 - img)

def threshold(img):
    img = cv_invert(img)
    throwaway, img = cv.threshold(img, 200, 255, cv.THRESH_BINARY)
    
    
    img = cv_invert(img)
    return img

def isolate_text(floorplan):
    
    kernel = np.ones((3,3),np.uint8)
    floorplan = cv_invert(floorplan)
    floorplan = cv_close(floorplan, kernel, depth=4)
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(floorplan)

    # UPPER_THRESHOLD = 750 # Hargadon text
    UPPER_THRESHOLD = 300 # Wendell_C text

    # remove large connected components
    floorplan[stats[labels, cv.CC_STAT_AREA] > UPPER_THRESHOLD] = 0
    return floorplan

def find_rooms(floorplan):
    kernel = np.ones((3,3),np.uint8)
    floorplan = cv_invert(cv.dilate(cv_invert(floorplan), kernel, iterations = 2))
    floorplan = cv_invert(cv.erode(cv_invert(floorplan), kernel, iterations = 2))
    cv.imwrite("debug.png", floorplan)
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(floorplan)
    LOWER_THRESHOLD = 40000
    UPPER_THRESHOLD = 1280000
    floorplan[stats[labels, cv.CC_STAT_AREA] > UPPER_THRESHOLD] = 0
    floorplan[stats[labels, cv.CC_STAT_AREA] < LOWER_THRESHOLD] = 0

    return floorplan


inFilename = sys.argv[1]
outFilename = sys.argv[2]

floorplan = cv.imread(inFilename,cv.IMREAD_GRAYSCALE)
floorplan = threshold(floorplan)


text = isolate_text(floorplan)
no_text = cv.add(floorplan, text)

rooms = find_rooms(no_text)



# write image

cv.imwrite("text.png", text)
cv.imwrite("rooms.png", rooms)

