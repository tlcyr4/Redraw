import os
import re
import sys
import json

import cv2 as cv
import numpy as np
from pytesseract import pytesseract as pt
from PIL import Image

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
        self.origin = (bbox[0],bbox[2])
    def draw(self, img, color = (0,0,255)):
        cv.drawContours(img, self.contours, 0, color, thickness = 5, offset = self.origin)
        centroid = (int(self.centroid[0]), int(self.centroid[1]))
        cv.putText(img, self.number, centroid, cv.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (255,0,0), thickness = 3)    
    def toJSON(self):
        return {"outline":self.contours[0].tolist(), "origin": self.origin, "number": self.number}

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
        rooms = self.invert(cv.morphologyEx(self.invert(no_text), cv.MORPH_CLOSE, self.kernel, iterations = 2))
        segments["rooms"] = Segment(rooms)
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
        kernel = np.ones((3,3),np.uint8)
        segments = self.segments
        rooms = segments["rooms"]
        for room_label in rooms.labels:
            if room_label == 0:
                continue
            left, right, top, bottom = rooms.bbox(room_label)
            roomlabels = rooms.labelled[top:bottom, left:right]

            inverted = np.copy(segments["no_text"].img[top:bottom,left:right])
            inverted[(roomlabels != room_label) & (roomlabels != 0)] = 255
            inverted[roomlabels == room_label] = 0
            inverted = cv.morphologyEx(inverted, cv.MORPH_CLOSE, kernel, iterations = 3)
            defects = Segment(inverted)
            defects.cc_threshold(5000, 20000)
            for defect_label in defects.labels:
                if defect_label == 0:
                    continue
                defect_left,defect_right,defect_top,defect_bottom = defects.bbox(defect_label)
                defect_box = inverted[defect_top:defect_bottom, defect_left:defect_right]
                defect_box, contours, hierarchy = cv.findContours(defect_box, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                correlation = cv.matchShapes(ref_door[0], contours[0], 1, 0.0)
                if correlation < corr_thresh:
                    bbox = [left+defect_left,left+defect_right,top+defect_top,top+defect_bottom]
                    centroid = defects.centroids[defect_label]
                    centroid = (int(centroid[0]), int(centroid[1]))
                    door = Door(bbox, contours, rooms.labelled[centroid[1],centroid[0]], room_label, (defect_left,defect_top))
                    self.doors.append(door)
    def transplant_doors(self, closing = 5):
        rooms = self.segments["rooms"]
        img = rooms.img
        labelled = rooms.labelled
        for door in self.doors:
            r_left,r_right,r_top,r_bottom = rooms.bbox(door.into)
            d_left,d_right,d_top,d_bottom = door.bbox

            # expand door-box
            d_left-=closing
            d_top-=closing
            d_bottom+=closing
            d_right+=closing

            subrect = img[d_top:d_bottom,d_left:d_right]
            subrect[subrect == subrect] = 0
            intersect = intersection(rooms.bbox(door.into), (d_left,d_right,d_top,d_bottom))
            subrect = img[intersect[2]:intersect[3],intersect[0]:intersect[1]]
            subrect[subrect == subrect] = 255
        # cv.imwrite('debug.png', img)
        self.segments["rooms"] = Segment(img)
                
def intersection(a,b):
  left = max(a[0], b[0])
  right = min(a[1], b[1])
  top = max(a[2], b[2])
  bottom = min(a[3], b[3])
  return (left,right,top,bottom)

def main():
    inFilename = sys.argv[1]
    outFilename = sys.argv[2]

    floornum = re.findall("[0-9][0-9].png", inFilename)[0][1]
    floor = Floor(cv.imread(inFilename, cv.IMREAD_COLOR), "door3.png", floornum = floornum)
    
    floor.segment(room_upper_thresh = None)
    # cv.imwrite('debug.png', floor.segments["rooms"].img)
    floor.find_doors()
    floor.transplant_doors()
    
    # for door in floor.doors:
    #     door.draw(floor.original)
    floor.find_rooms()
    for room in floor.rooms:
        room.draw(floor.original)
    
    json.dump([room.toJSON() for room in floor.rooms], open(outFilename, "w"))
    cv.imwrite("debug.png", floor.original)

   

main()