import os
import re
import sys
import json
import random
import time
import glob
import winsound

import cv2 as cv
import numpy as np
from pytesseract import pytesseract as pt
from PIL import Image

global verbose, efr, cluttered, totalTime, timing, missed

def randColor():
    return tuple(random.sample(xrange(128,256),3))

class Door:
    def __init__(self, bbox, contours, outof, into, rel_origin):
        self.bbox = bbox
        self.contours = contours
        self.outof = outof
        self.into = into
        self.origin = (bbox[0],bbox[2])
        self.rel_origin = rel_origin
    def draw(self, img, color = (0,255,0)):
        cv.drawContours(img, self.contours, 0, color, thickness = -1, offset = self.origin)

class Room:
    def __init__(self, bbox, label, centroid, area, number, contours):
        self.bbox = bbox
        self.label = label
        self.centroid = centroid
        self.area = area
        self.number = number
        self.contours = contours
        self.poly = cv.approxPolyDP(self.contours[0],10,True)
        self.origin = (bbox[0],bbox[2])
    def draw(self, img, color = (0,0,255)):
        # cv.drawContours(img, self.contours, 0, color, thickness = 5, offset = self.origin)
        cv.drawContours(img, [self.poly], 0, color, thickness = 5, offset = self.origin)
        centroid = (int(self.centroid[0]), int(self.centroid[1]))
        cv.putText(img, self.number, centroid, cv.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (255,0,0), thickness = 3)    
    def toJSON(self):
        return {"outline":self.poly.tolist(), "origin": self.origin, "number": self.number}

class Segment:
    def __init__(self, img):
        self.img = img
        self.num_ccs, self.labelled, self.stats, self.centroids = cv.connectedComponentsWithStats(img)
        self.labels = np.unique(self.labelled)
    def cc_threshold(self, lower = None, upper = None):
        if upper != None:
            self.img[self.stats[self.labelled, cv.CC_STAT_AREA] > upper] = 0
            self.labels = self.labels[self.stats[self.labels, cv.CC_STAT_AREA] <= upper]
        if lower != None:
            self.img[self.stats[self.labelled, cv.CC_STAT_AREA] < lower] = 0
            self.labels = self.labels[self.stats[self.labels, cv.CC_STAT_AREA] >= lower]
    def bbox(self, label):
        left = self.stats[label, cv.CC_STAT_LEFT]
        right = left + self.stats[label,cv.CC_STAT_WIDTH]
        top = self.stats[label, cv.CC_STAT_TOP]
        bottom = top + self.stats[label, cv.CC_STAT_HEIGHT]
        return left, right, top, bottom
    def convex_hull(self, label):
        left,right,top,bottom = self.bbox(label)
        cutout = np.copy(self.img[top:bottom,left:right])
        sublabelled = self.labelled[top:bottom, left:right]
        cutout[sublabelled != label] = 0
        # cv.imwrite("not" + str(label) + ".png", cutout)
        contours = cv.findContours(cutout, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]
        return [cv.convexHull(contours[0])]
    def colored(self):
        canvas = cv.cvtColor(np.zeros(self.img.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
        for label in self.labels:
            if label != 0:
                canvas[self.labelled == label] = randColor()
                centroid = (int(self.centroids[label][0]), int(self.centroids[label][1]))
                cv.putText(canvas, str(label), centroid, cv.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (10,10,10), thickness = 3) 
        return canvas


class Floor:
    def __init__(self, img, ref_door_filename, floornum = 1):
        self.kernel = np.ones((3,3),np.uint8)
        self.original = img
        self.floornum = floornum
        self.rooms = []
        self.doors = []
        self.segments = {}
        door = cv.imread(ref_door_filename, cv.IMREAD_GRAYSCALE)
        door, self.ref_door, hierarchy = cv.findContours(door, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    def invert(self, img):
        """ Flips black and white """
        return (255 - img)
    def segment(self, text_thresh = 300, room_lower_thresh = 20000, room_upper_thresh = 128000, lum_thresh = 200):
        """ populates segments dictionary with image segments 
            e.g. image with text filtered out"""
        segments = self.segments

        # thresholding
        thresholded = cv.cvtColor(self.original, cv.COLOR_RGB2GRAY)
        thresholded = self.invert(thresholded)
        throwaway, thresholded = cv.threshold(thresholded, lum_thresh, 255, cv.THRESH_BINARY)
        thresholded = self.invert(thresholded)
        segments["threshold"] = Segment(thresholded)

        # segment text
        text = cv.morphologyEx(self.invert(thresholded), cv.MORPH_CLOSE, self.kernel, iterations = 1)
        segments["text"] = Segment(text)
        segments["text"].cc_threshold(upper = text_thresh)
        no_text = cv.add(thresholded, text)
        segments["no_text"] = Segment(no_text)

        # segment rooms
        # cv.imwrite("before.png", segments["no_text"].colored())
        rooms = self.invert(cv.morphologyEx(self.invert(no_text), cv.MORPH_CLOSE, self.kernel, iterations = 2))
        segments["rooms"] = Segment(rooms)
        # cv.imwrite("after.png", segments["rooms"].colored())
        segments["rooms"].cc_threshold(room_lower_thresh, room_upper_thresh)

    def find_rooms(self):
        segments = self.segments
        kernel = np.ones((3,3),np.uint8)
        os.environ["TESSDATA_PREFIX"] = ".\\"
        rooms = segments["rooms"]
        for room_label in segments["rooms"].labels:
            if room_label == 0:
                continue # 0 denotes the blackness
            left, right, top, bottom = rooms.bbox(room_label)

            # take piece from text segment
            room_box = np.copy(segments["text"].img[top:bottom, left:right])
            roomlabels = rooms.labelled[top:bottom, left:right]
            # filter out other cc's that hang into box
            room_box[roomlabels != room_label] = 0

            # convert to PIL format for Tesseract
            pil_img = Image.fromarray(room_box)
            text = pt.image_to_string(pil_img).encode("utf-8").strip()
            if efr:
                roomnums = re.findall("[0-9]" + self.floornum + "[0-9]", text)
            elif two_digit:
                roomnums = re.findall("[0-9][0-9]", text)
            else:
                roomnums = re.findall(self.floornum + "[0-9][0-9]", text)
            if roomnums == []:
                roomnum = None
            else:
                roomnum = roomnums[0]
            
            # found a room number
            copy = np.copy(segments["rooms"].img[top:bottom, left:right]) # defensive copy for findContours
            copy[roomlabels != room_label] = 0
            if roomnum == None:
                continue
            copy, contours, hierarchy = cv.findContours(copy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            if contours == False:
                continue
            centroid = rooms.centroids[room_label]
            area = rooms.stats[room_label, cv.CC_STAT_AREA]
            room = Room(rooms.bbox(room_label), room_label, centroid, area, roomnum, contours)
            # self.spaces.append(room)
            if roomnum != None:
                self.rooms.append(room)
    def find_doors(self, corr_thresh = .025):
        ref_door = self.ref_door

        blah, ref_slant, hierarchy = cv.findContours(cv.imread("slant.png", cv.IMREAD_GRAYSCALE), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        blah, ref_halfdoor, hierarchy = cv.findContours(cv.imread("halfdoor.png", cv.IMREAD_GRAYSCALE), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        segments = self.segments
        rooms = segments["rooms"]
        if verbose:
            defect_canvas = cv.cvtColor(np.zeros(rooms.img.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            # cv.imwrite("prerooms.png", rooms.colored())
        for room_label in rooms.labels:
            if room_label == 0:
                continue # skip the blackness

            # cut out room labels
            left, right, top, bottom = rooms.bbox(room_label)
            roomlabels = rooms.labelled[top:bottom, left:right]

            # isolate whiteness of other connected components
            inverted = np.copy(segments["no_text"].img[top:bottom,left:right])

            inverted[roomlabels == room_label] = 0

            # seal up gaps left by gray cabinets in Whitman
            if cluttered:
                inverted = cv.morphologyEx(inverted, cv.MORPH_CLOSE, self.kernel, iterations = 3)
            if closedoor:
                inverted = cv.morphologyEx(inverted, cv.MORPH_OPEN, self.kernel, iterations = 3)
            # filter out everything not in the convex hull of the room
            hull = rooms.convex_hull(room_label)
            hullDrawing = cv.cvtColor(np.zeros(roomlabels.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            hullDrawing = cv.drawContours(hullDrawing, hull, 0, (255,255,255), thickness = -1)
            hullDrawing = cv.cvtColor(hullDrawing, cv.COLOR_RGB2GRAY)
            
            inverted = cv.bitwise_and(inverted, hullDrawing)
            

            defects = Segment(inverted)
            defects.cc_threshold(2250, 25000)
            
            for defect_label in defects.labels:
                if defect_label == 0:
                    continue
                defect_left,defect_right,defect_top,defect_bottom = defects.bbox(defect_label)
                defect_box = inverted[defect_top:defect_bottom, defect_left:defect_right]
                defect_box, contours, hierarchy = cv.findContours(defect_box, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                correlation = cv.matchShapes(ref_door[0], contours[0], 1, 0.0)
                correlation = min(correlation, cv.matchShapes(ref_slant[0], contours[0], 1, 0.0))
                correlation = min(correlation, cv.matchShapes(ref_halfdoor[0], contours[0], 1, 0.0))

                if verbose:
                    defect_canvas = cv.drawContours(defect_canvas, contours, 0, randColor(), -1, offset = (left+defect_left,top+defect_top))
                if correlation < corr_thresh:
                    bbox = [left+defect_left,left+defect_right,top+defect_top,top+defect_bottom]
                    centroid = defects.centroids[defect_label]
                    centroid = (int(centroid[0]), int(centroid[1]))
                    door = Door(bbox, contours, rooms.labelled[centroid[1],centroid[0]], room_label, (defect_left,defect_top))
                    self.doors.append(door)
                    
        if verbose:
            cv.imwrite("defects.png", defect_canvas)
    def transplant_doors(self, closing = 5):
        """ cuts doors out of the rooms their attached to 
            and stitches them into the ones they stick into """
        rooms = self.segments["rooms"]
        img = rooms.img
        labelled = rooms.labelled
        for door in self.doors:
            r_left,r_right,r_top,r_bottom = rooms.bbox(door.into)
            cutout = img[r_top-closing:r_bottom+closing,r_left-closing:r_right+closing]

            # draw room's convex hull on its own canvas
            room_hull = rooms.convex_hull(door.into)
            room_hull_pic = cv.cvtColor(np.zeros(cutout.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            cv.drawContours(room_hull_pic, room_hull, 0, (255,255,255), thickness=-1, offset=(closing,closing))
            room_hull_pic = cv.cvtColor(room_hull_pic, cv.COLOR_RGB2GRAY)

            # draw door in its own canvas and dilate
            offset = (door.rel_origin[0]+closing, door.rel_origin[1]+closing)
            door_canvas = cv.cvtColor(np.zeros(cutout.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            door_canvas = cv.drawContours(door_canvas, door.contours, 0, (255,255,255), thickness=-1, offset =offset)
            door_canvas = cv.cvtColor(door_canvas, cv.COLOR_RGB2GRAY)
            door_canvas = cv.dilate(door_canvas, self.kernel, iterations = closing)

            # take intersection of two
            intersect = cv.bitwise_and(door_canvas, room_hull_pic)

            # update labels
            sublabelled = labelled[r_top-closing:r_bottom+closing,r_left-closing:r_right+closing]
            sublabelled[intersect == 255] = door.into

            # black out door's rect and whiten intersection
            cv.bitwise_and(cutout, cv.bitwise_not(door_canvas), cutout)
            cv.bitwise_or(cutout, intersect, cutout)


        # cv.imwrite('debug.png', img)
        self.segments["rooms"] = Segment(img)

def main(inFilename):
    global verbose, efr, cluttered, totalTime, timing, missed, two_digit, closedoor, unmarked
    outFilename = "results\\" + inFilename.split("\\")[-1]
    building = inFilename.split("\\")[-2]
    efr = building  in "1915 Hamilton Joline 1901_Laughlin 1903 Cuyler Foulke Henry Lockhart Pyne 1927_Clapp 1937 1938 Dodge_Osborn Walker"
    two_digit = building in "Campbell Blair Little Buyers Holder Dickinson Patton Spelman Wright"
    closedoor = building in "Campbell"
    cluttered = building in "Wendell_B Wendell_C"
    unmarked = building in  "Blair Joline Campbell Alexander Cuyler Foulke Henry Lockhart Patton Scully Spelman Wright 1938 Feinberg"

    if timing:
        start = time.clock()

    floornum = re.findall(".\.png", inFilename)[0][0]
    floor = Floor(cv.imread(inFilename, cv.IMREAD_COLOR), "door3.png", floornum = floornum)
    
    floor.segment(room_upper_thresh = None, text_thresh=2200)
    # cv.imwrite('debug.png', floor.segments["rooms"].img)
    floor.find_doors(corr_thresh = .03)
    floor.transplant_doors()
    
    for door in floor.doors:
        door.draw(floor.original)
    floor.find_rooms()
    for room in floor.rooms:
        room.draw(floor.original)
    
    jsonFilename = outFilename.split(".")[0]+".json"
    json.dump([room.toJSON() for room in floor.rooms], open(jsonFilename, "w"))
    cv.imwrite(outFilename, floor.original)
    if timing:
        t = time.clock() - start
        totalTime += t
        try:
            print "Wall Clock Time: ", t
        except:
            missed += t
    if verbose:
        cv.imwrite("rooms.png", floor.segments["rooms"].colored())
        cv.imwrite("text.png", floor.segments["text"].img)
        cv.imwrite("no_text.png", floor.segments["no_text"].img)


verbose = "-v" in sys.argv
efr = "-efr" in sys.argv
cluttered = "-cluttered" in sys.argv
timing = "-time" in sys.argv

totalTime = 0
missed = 0
inFiles = glob.glob(sys.argv[1])
# count = 0
for inFilename in inFiles:
    main(inFilename)
    # print inFilename
    # outFilename = "results\\" + inFilename.split("\\")[-1]
    # print outFilename
    # count += 1
    # print re.findall(".\.png", inFilename)[0][0]
# print count
if timing:
    print "missed: ", missed
    print "total time: ", totalTime
winsound.Beep(600, 250)