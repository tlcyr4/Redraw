import cv2 as cv
import numpy as np
import sys
from pytesseract import pytesseract as pt
from PIL import Image
import os
import re
kernel = np.ones((3,3),np.uint8)
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
    
    floorplan = cv_invert(cv.dilate(cv_invert(floorplan), kernel, iterations = 2))
    floorplan = cv_invert(cv.erode(cv_invert(floorplan), kernel, iterations = 2))
    
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(floorplan)
    LOWER_THRESHOLD = 40000
    UPPER_THRESHOLD = 1280000
    floorplan[stats[labels, cv.CC_STAT_AREA] > UPPER_THRESHOLD] = 0
    floorplan[stats[labels, cv.CC_STAT_AREA] < LOWER_THRESHOLD] = 0

    return floorplan


inFilename = sys.argv[1]
outFilename = sys.argv[2]

floor = re.findall("[0-9][0-9].png", inFilename)[0][1]

floorplan = cv.imread(inFilename,cv.IMREAD_GRAYSCALE)
floorplan = threshold(floorplan)


text = isolate_text(floorplan)
no_text = cv.add(floorplan, text)

rooms_only = find_rooms(no_text)

retval, labels, stats, centroids = cv.connectedComponentsWithStats(rooms_only)

cv.imwrite("debug.png", rooms_only)

# start ocr

os.environ["TESSDATA_PREFIX"] = ".\\"

inverted = cv_invert(floorplan)
inverted = cv_close(inverted, kernel)

in_color = cv.cvtColor(floorplan, cv.COLOR_GRAY2RGB)

for i in range(1,len(stats)):
    left = stats[i, cv.CC_STAT_LEFT]
    right = left + stats[i,cv.CC_STAT_WIDTH]
    top = stats[i, cv.CC_STAT_TOP]
    bottom = top + stats[i, cv.CC_STAT_HEIGHT]

    subrect = text[top:bottom, left:right]

    img = Image.fromarray(subrect)
    output = pt.image_to_string(img).encode("utf-8").strip()
    roomnums = " ".join(re.findall(floor + "[0-9][0-9]", output))
    if len(roomnums) > 0:
        cv.rectangle(in_color, (left, top), (right, bottom), (0,0,255), 10)
        print roomnums

    # cv.imwrite("subrect" + str(i) + ".png", subrect)



cv.imwrite("debug.png", in_color)

# write image

cv.imwrite("text.png", text)
cv.imwrite("rooms.png", rooms_only)

