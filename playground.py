import cv2 as cv
import numpy as np
import pytesseract

def cv_close(img, kernel, depth = 1):
    return cv.erode(cv.dilate(img, kernel, depth), kernel, depth)


def cv_open(img, kernel, depth = 1):
    return cv.dilate(cv.erode(img, kernel, depth), kernel, depth)

floorplan = cv.imread('PNG/Whitman/Wendell_C/0670-02.png',cv.IMREAD_GRAYSCALE)

# kernel for any convolution
kernel = np.ones((3,3),np.uint8)

# flip black and white
floorplan = (255 - floorplan)

# apply thresholding to remove grays
throwaway, floorplan = cv.threshold(floorplan, 200, 255, cv.THRESH_BINARY)

# fill in some gaps
floorplan = cv_close(floorplan, kernel, depth=4)

# run connected component analysis
retval, labels, stats, centroids = cv.connectedComponentsWithStats(floorplan)

# value slightly bigger than text characters
# CHARACTER_THRESHOLD = 750 # Hargadon
CHARACTER_THRESHOLD = 300 # Wendell_C
# remove large connected components
cv.imwrite("debug.png", floorplan)

floorplan[stats[labels, cv.CC_STAT_AREA] > CHARACTER_THRESHOLD] = 0

# write image
cv.imwrite("temp.png", 255 - floorplan)

