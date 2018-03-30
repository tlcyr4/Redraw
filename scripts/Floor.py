import os
import re

import cv2 as cv
import numpy as np
from pytesseract import pytesseract as pt
from PIL import Image

from Segment import Segment
from Door import Door
from Room import Room
from shortcuts import *

class Floor:
    def __init__(self, img, floornum, building):
        self.kernel = np.ones((3,3),np.uint8)
        self.original = img
        self.floornum = floornum
        self.rooms = {}
        self.doors = []
        self.segments = {}
        self.building = building
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
    def find_rooms(self, efr, two_digit):
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
                roomnums = re.findall("[0-9][0-9][0-9]?", text)
            else:
                roomnums = re.findall(self.floornum + "[0-9][0-9]", text)
            if roomnums != []:
                self.rooms[room_label] = Room(rooms, room_label, roomnums[0], self.building)
    def find_doors(self, cluttered, close_door, corr_thresh = .025):
        rdfs = ("door3.png", "slant.png", "halfdoor.png")
        ref_doors = [find_border(cv.imread(f, cv.IMREAD_GRAYSCALE)) for f in rdfs]
        segments = self.segments
        rooms = segments["rooms"]
        # if verbose:
        #     defect_canvas = cv.cvtColor(np.zeros(rooms.img.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
        for room_label in rooms.labels:
            if room_label == 0: continue # skip the blackness

            # cut out room labels
            left, right, top, bottom = rooms.bbox(room_label)
            roomlabels = rooms.labelled[top:bottom, left:right]

            # isolate whiteness of other connected components
            inverted = np.copy(segments["no_text"].img[top:bottom,left:right])
            inverted[roomlabels == room_label] = 0

            # seal up gaps left by gray cabinets in Whitman
            if cluttered:
                cv.morphologyEx(inverted, cv.MORPH_CLOSE, self.kernel, inverted, iterations = 3)
            if close_door:
                cv.morphologyEx(inverted, cv.MORPH_OPEN, self.kernel, inverted, iterations = 3)
            
            # filter out everything not in the convex hull of the room
            hull = rooms.convex_hull(room_label)
            hullDrawing = cv.cvtColor(np.zeros(roomlabels.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            hullDrawing = cv.drawContours(hullDrawing, hull, 0, WHITE, thickness = -1)
            hullDrawing = cv.cvtColor(hullDrawing, cv.COLOR_RGB2GRAY)
            
            inverted = cv.bitwise_and(inverted, hullDrawing)
            

            defects = Segment(inverted)
            defects.cc_threshold(2250, 25000)
            
            for defect_label in defects.labels:
                if defect_label == 0:
                    continue
                defect_left,defect_right,defect_top,defect_bottom = defects.bbox(defect_label)
                defect_cutout = defects.cutout(defect_label)
                contours = find_border(defect_cutout)
                
                correlation = min([cv.matchShapes(ref_door[0], contours[0], 1, 0.0) for ref_door in ref_doors])

                # if verbose:
                #     defect_canvas = cv.drawContours(
                #         image = defect_canvas, 
                #         contours = contours, 
                #         contourIdx = 0, 
                #         color = randColor(), 
                #         thickness = cv.FILLED, 
                #         offset = (left+defect_left,top+defect_top)
                #         )
                if correlation < corr_thresh:
                    bbox = [left + defect_left,
                            left + defect_right,
                            top + defect_top,
                            top + defect_bottom]
                    centroid = tuple(map(int, defects.centroids[defect_label]))
                    door = Door(bbox, contours, rooms.labelled[centroid[::-1]], room_label, (defect_left,defect_top))
                    self.doors.append(door)
                    
        # if verbose:
        #     cv.imwrite("defects.png", defect_canvas)
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
            offset = (door.getRelOrigin()[0]+closing, door.getRelOrigin()[1]+closing)
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

            # update centroid and area
            isolate = np.zeros(img.shape, dtype="uint8")
            isolate[labelled == door.into] = 255

            # cv.imwrite("debug.png", isolate)
            blah, bleh, stats, centroids = cv.connectedComponentsWithStats(isolate)
            rooms.stats[door.into] = stats[1, :]
            rooms.centroids[door.into] = centroids[1]
    def toJSON(self):
        return [{"polygon":room.getPoly().tolist(), 
                "origin": room.getOrigin(), 
                "number": room.number, 
                "building": self.building.upper(), 
                "floor": self.floornum} for room in self.rooms.values()]
    def draw_doors(self):
        for door in self.doors:
            door.draw(self.original)
    def draw_rooms(self):
        for room in self.rooms.values():
            room.draw(self.original)