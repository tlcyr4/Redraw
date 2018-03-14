import os
import re
import sys

import cv2 as cv
import numpy as np
from pytesseract import pytesseract as pt
from PIL import Image

TRIM = 2 # pixels to trim off of convex defect because of walls


def cv_close(img, kernel, depth = 1):
    temp = cv.dilate(img, kernel, depth)
    return cv.erode(temp, kernel, depth)

def cv_open(img, kernel, depth = 1):
    return cv.dilate(cv.erode(img, kernel, depth), kernel, depth)

def cv_invert(img):
    return (255 - img)

def threshold(img):
    img = cv_invert(img)
    throwaway, img = cv.threshold(img, 200, 255, cv.THRESH_BINARY)
    img = cv_invert(img)
    return img

def segment_text(floorplan):
    kernel = np.ones((3,3),np.uint8)
    floorplan = cv_invert(floorplan)
    floorplan = cv.morphologyEx(floorplan, cv.MORPH_CLOSE, kernel, iterations = 1)
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(floorplan)

    # UPPER_THRESHOLD = 750 # Hargadon text
    UPPER_THRESHOLD = 300 # Wendell_C text

    # remove large connected components
    floorplan[stats[labels, cv.CC_STAT_AREA] > UPPER_THRESHOLD] = 0
    return floorplan

def segment_rooms(floorplan):
    kernel = np.ones((3,3),np.uint8)
    floorplan = cv_invert(cv.dilate(cv_invert(floorplan), kernel, iterations = 2))
    floorplan = cv_invert(cv.erode(cv_invert(floorplan), kernel, iterations = 2))
    
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(floorplan)
    LOWER_THRESHOLD = 20000
    UPPER_THRESHOLD = 1280000
    # floorplan[stats[labels, cv.CC_STAT_AREA] > UPPER_THRESHOLD] = 0
    floorplan[stats[labels, cv.CC_STAT_AREA] < LOWER_THRESHOLD] = 0

    return floorplan

def segment_floorplan(floorplan):
    segments = {}
    segments["threshold"] = threshold(floorplan)
    segments["text"] = segment_text(segments["threshold"])
    segments["no_text"] = cv.add(segments["threshold"], segments["text"])
    segments["rooms"] = segment_rooms(segments["no_text"])
    return segments

def ocr_rooms(segments, floor, in_color):
    kernel = np.ones((3,3),np.uint8)
    os.environ["TESSDATA_PREFIX"] = ".\\"
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(segments["rooms"])
    rooms = {}
    for i in range(1,len(stats)):
        left = stats[i, cv.CC_STAT_LEFT]
        right = left + stats[i,cv.CC_STAT_WIDTH]
        top = stats[i, cv.CC_STAT_TOP]
        bottom = top + stats[i, cv.CC_STAT_HEIGHT]

        subrect = np.copy(segments["text"][top:bottom, left:right])
        sublabels = labels[top:bottom, left:right]
        subrect[sublabels != i] = 0

        pil_img = Image.fromarray(subrect)
        output = pt.image_to_string(pil_img).encode("utf-8").strip()
        roomnums = re.findall(floor + "[0-9][0-9]", output)
        if len(roomnums) > 0:
            box = ((left, top), (right, bottom))
            if roomnums[0] not in rooms:
                rooms[roomnums[0]] = []
            rooms[roomnums[0]].append(box)
            subrect = in_color[top:bottom, left:right]
            copy = cv.cvtColor(np.copy(subrect), cv.COLOR_RGB2GRAY)
            copy[sublabels!= i] = 0
            copy, contours, hierarchy = cv.findContours(copy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cv.drawContours(subrect, contours, 0, (0,0,255), thickness = 5)
    return rooms

def find_doors(segments, in_color):
    door = cv.imread('door3.png', cv.IMREAD_GRAYSCALE)
    door, door_contours, hierarchy = cv.findContours(door, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)


    kernel = np.ones((3,3),np.uint8)
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(segments["rooms"])
    for i in range(1,len(stats)):
        left = stats[i, cv.CC_STAT_LEFT]
        right = left + stats[i,cv.CC_STAT_WIDTH]
        top = stats[i, cv.CC_STAT_TOP]
        bottom = top + stats[i, cv.CC_STAT_HEIGHT]

        sublabels = labels[top:bottom, left:right]

        flipped = np.copy(segments["no_text"][top:bottom, left:right])
        flipped[(sublabels != i) & (sublabels != 0)] = 255
        flipped[sublabels == i] = 0
        flipped = cv.morphologyEx(flipped, cv.MORPH_CLOSE, kernel, iterations = 3)
        retval, defects, defect_stats, defect_centroid = cv.connectedComponentsWithStats(flipped)
        for j in np.unique(defects):
            if j == 0:
                continue
            cc_left = defect_stats[j, cv.CC_STAT_LEFT]
            cc_right = cc_left + defect_stats[j,cv.CC_STAT_WIDTH]
            cc_top = defect_stats[j, cv.CC_STAT_TOP]
            cc_bottom = cc_top + defect_stats[j, cv.CC_STAT_HEIGHT]
            defect_box = flipped[cc_top:cc_bottom, cc_left:cc_right]
            if defect_stats[j, cv.CC_STAT_AREA] > 5000 and defect_stats[j, cv.CC_STAT_AREA] < 20000:
                defect_box, contours, hierarchy = cv.findContours(defect_box, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                dooryness = cv.matchShapes(door_contours[0], contours[0], 1, 0.0)    

                if dooryness > .025:# or dooryness == 0.0: seems to be the return value for failure
                    continue

                defect_box = cv.cvtColor(defect_box, cv.COLOR_GRAY2RGB)
                
                subrect = in_color[top+cc_top:top + cc_bottom, left+cc_left:left + cc_right]
                cv.drawContours(subrect, contours, 0, (0,255,0), thickness = 5)

def main():
    inFilename = sys.argv[1]
    outFilename = sys.argv[2]

    floor = re.findall("[0-9][0-9].png", inFilename)[0][1]
    floorplan = cv.imread(inFilename,cv.IMREAD_GRAYSCALE)
    in_color = cv.cvtColor(floorplan, cv.COLOR_GRAY2RGB)


    segments = segment_floorplan(floorplan)
    

    
    rooms = ocr_rooms(segments, floor, in_color)
    doors = find_doors(segments, in_color)

    # f = open("rooms.txt", 'w')
    # for number in rooms:
    #     for subroom in rooms[number]:
    #         cv.rectangle(in_color, subroom[0], subroom[1], (0,0,255), 10)
    #     f.write(str(number) + ': ' + str(rooms[number]) + '\n')

    cv.imwrite(outFilename, in_color)
    cv.imwrite("text.png", segments["text"])
    cv.imwrite("no_text.png", segments["no_text"])
    cv.imwrite("rooms.png", segments["rooms"])

main()