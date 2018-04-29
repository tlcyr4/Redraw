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
    def __init__(self, img, floornum, building,preprocessed=False):
        self.kernel = np.ones((3,3),np.uint8)
        self.original = img
        self.floornum = floornum
        self.rooms = {}
        self.doors = []
        self.segments = {}
        self.building = building
        self.preprocessed=preprocessed
    def invert(self, img):
        """ Flips black and white """
        return (255 - img)
    def segment(self, text_thresh = 300, room_lower_thresh = 20000, room_upper_thresh = 128000, lum_thresh = 200):
        """ populates segments dictionary with image segments 
            e.g. image with text filtered out"""
        segments = self.segments

        if self.building == "0053" and self.floornum in "01 02":
            lum_thresh = 100
        # thresholding
        thresholded = cv.cvtColor(self.original, cv.COLOR_RGB2GRAY)
        if self.building == "0703":
            print "fuck"
            throwaway, thresholded = cv.threshold(thresholded, 1, 255, cv.THRESH_BINARY)
        thresholded = self.invert(thresholded)
        if not self.preprocessed:
            throwaway, thresholded = cv.threshold(thresholded, lum_thresh, 255, cv.THRESH_BINARY)
            thresholded = self.invert(thresholded)
        segments["threshold"] = Segment(thresholded)

        if self.building == "0053" and self.floornum in "01 02":
            pass
            print "thin other"
            thresholded = cv.dilate(self.invert(thresholded), self.kernel, iterations=1)
            thresholded = self.invert(thresholded)

        # segment text
        text = cv.morphologyEx(self.invert(thresholded), cv.MORPH_CLOSE, self.kernel, iterations = 1)
        segments["text"] = Segment(text)
        segments["text"].cc_threshold(upper = text_thresh)
        no_text = cv.add(thresholded, text)
        segments["no_text"] = Segment(no_text)

        
        # segment rooms
        if self.floornum == "1" and self.building == "0148":
            print "thin"
            no_text = cv.dilate(self.invert(no_text), self.kernel, iterations=1)
            no_text = self.invert(no_text)
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
            text = text.replace("O","0")
            text = text.replace("I","1")
            text = text.replace("Z", "2")
            text = text.replace("1 1","11")

            if self.building == "0014":
                text = text.replace(" ","")
                if self.floornum == "2" and room_label == 110:
                    continue
                if self.floornum == "3" and room_label == 113:
                    continue
                if self.floornum == "4" and room_label == 123:
                    continue
            # if self.building == "0021" and room_label == self.num_ccs
            if self.building == "0021":
                if self.floornum == "0" and room_label == 803:
                    continue
                if self.floornum == "2" and room_label == 1:
                    continue
            if self.building == "0023":
                if self.floornum == "0" and room_label == 626:
                    continue
                if self.floornum == "2" and room_label == 405:
                    continue
                if self.floornum == "3" and room_label == 500:
                    continue
            # if self.building == "0026"
            if "112" in text and room_label == 79 and self.building == "0012":
                continue
            if False:
                print text

            if self.building == "0095":
                roomnums = re.findall("[0-9][0-9][0-9]", text)
            if self.building in ["0030","0040","0053"] and self.floornum == "A":
                roomnums = re.findall("[0-9]0[0-9]", text)
            elif self.building == "0012":
                roomnums = re.findall("[0-9][0-9][0-9][NS]?", text.replace("8","S"))
            elif self.building == "0019" and self.floornum == "A":
                roomnums = re.findall("[B8][0-9][0-4]", text)
                if roomnums != [] and roomnums[0][0] == "8":
                    roomnums[0] = "B" + roomnums[0][1:]
            elif self.building == "0019" and self.floornum == "2":
                roomnums = re.findall("1?[A0-9][0-9]", text)
                if roomnums != [] and roomnums[0][0] == "A":
                    roomnums[0] = "A02"
            elif self.building == "0021" and self.floornum == "0":
                roomnums = re.findall("A[0-9][0-9]", text)
            elif self.building == "0023":
                roomnums = re.findall("["+self.floornum +"]?[0-9][0-9]|T[01][0-9]", text)
            elif self.building == "0026":
                if self.floornum == "3":
                    roomnums = re.findall("[0-9]..?.?[ABC]", text)
                    if roomnums == []:
                        continue
                    roomnums[0] = re.sub(r'\W+', '', roomnums[0])
                    roomnums[0] = "00" + roomnums[0][:2]
                else:
                    if self.floornum == "2" and "5" in text:
                        text = text.replace("8", "B")
                    roomnums = re.findall("["+self.floornum +"][0-9][0-9]|[1-9][0-9][AB]?", text)
                    if roomnums != [] and (roomnums[0] == "52A" or roomnums[0] == "52B"):
                        roomnums[0] = "0" + roomnums[0]
            elif self.building == "0019":
                roomnums = re.findall("[1"+self.floornum +"][0-9][0-9]|[1-9AT][0-9]", text)
                if self.floornum == "4":
                    roomnums = re.findall("T[0-9]", text.replace("S","6"))
                if roomnums != [] and (roomnums[0] == "T0" or roomnums[0] in "A1 160"):
                    continue
            elif self.building == "0028" and self.floornum == "3":
                roomnums = re.findall("1[0-4][0-9]|[2-9][0-9]", text)
                if room_label == 145:
                    roomnums = ["116"]
            elif "004" in self.building or self.building == "0053":
                roomnums = re.findall("[0-9]" + self.floornum + "[0-9]A?", text)
                if self.building == "0043" and self.floornum == "0" and room_label == 23:
                    roomnums = ["104"]
            elif self.building == "0092" and self.floornum == "1":
                roomnums = re.findall("[0-9]" + self.floornum + "[0-9]", text)
                override = {30:"112",67:"113",102:"114"}
                if room_label in override:
                    roomnums = [override[room_label]]
            elif self.building == "0148":
                if self.floornum == "3":
                    if room_label == 827:
                        roomnums = []
                    roomnums = re.findall("3[0-9][0-9]", text.replace("35","36"))
            elif self.building == "0603":
                roomnums = re.findall(self.floornum + "[0-9][0-9]", text)
                if self.floornum == "1":
                    if room_label in [822,823]:
                        roomnums = ["101"]
                    if room_label in [1166,1224,1423]:
                        roomnums = ["122"]
                if self.floornum == "2":
                    if room_label in [1044,1045]:
                        roomnums = ["201"]
                    if room_label in [44,58,103]:
                        roomnums = ["272"]
                    if room_label in [1535,1660]:
                        roomnums = ["222"]
                    if room_label in [1522,1725,1751]:
                        rooomnums = ["202"]
                if self.floornum == "3":
                    if room_label in [1330,1331]:
                        roomnums = ["301"]
                    if room_label in [1810,1951]:
                        roomnums = ["322"]
            elif self.building == "0619" and (self.floornum == "2" or self.floornum == "1"):
                roomnums = re.findall("T?[0-9][0-9]", text)
            elif self.building == "0631" and self.floornum == "A":
                roomnums = re.findall("B?[0-9][0-9]", text.replace("8","B"))
                if roomnums != [] and len(roomnums[0]) < 3:
                    roomnums[0] = "B" + roomnums[0]
                if room_label == 222:
                    roomnums = ["B21"]
            elif self.building == "0631" and self.floornum == "2":
                roomnums = re.findall("[0-9][0-9]|T[0-9]", text)
                if roomnums != [] and roomnums[0][0] == "T":
                    roomnums[0] = "T02"
            elif self.building == "0668" and self.floornum == "0":
                roomnums = re.findall("0[0-9][0-9]", text)
                if room_label == 384:
                    roomnums = ["027"]
            elif self.building == "0668" and self.floornum == "3":
                roomnums = re.findall("3[0-9][0-9]", text)
                if room_label in [25,29,26,33,35]:
                    roomnums = ["301"]
                if room_label in [41,46]:
                    roomnums = ["302"]
            elif self.building == "0672":
                roomnums = re.findall(self.floornum+"[01][0-9][ABCD]?", text.replace("8","B").replace("GB","G3").replace("0B","03"))
            elif self.building == "0686" and self.floornum == "4":
                roomnums = re.findall("4[0-9][0-9]", text)
                if room_label in [22,57,128]:
                    roomnums = ["402"]
                if room_label in [129]:
                    roomnums = ["404"]
                if room_label in [130]:
                    roomnums = ["406"]
                if room_label in [34]:
                    roomnums = ["401"]
            elif self.building == "0694" and self.floornum == "3":
                roomnums = re.findall("3[0-9][0-9]?", text)
                if room_label in [38,129,139,207]:
                    roomnums = ["302"]
                if room_label in [211]:
                    roomnums = ["303"]
                if room_label in [225]:
                    roomnums = ["304"]
                if room_label in [244]:
                    roomnums = ["305"]
            elif self.building == "0695" and self.floornum == "1":
                roomnums = re.findall("1[0-9][0-9]?", text)
                if room_label in [3,7,14,37]:
                    roomnums = ["104"]
                if room_label in [50,60,68,97]:
                    roomnums = ["102"]
                if room_label in [51,59,67,137]:
                    roomnums = ["101"]
            elif self.building == "0696" and self.floornum == "1":
                roomnums = re.findall("1[0-9][0-9]?", text)
                if room_label in [784]:
                    roomnums = ["105"]
                if room_label in [887,948]:
                    roomnums = ["107"]
                if room_label in [874]:
                    roomnums = ["106"]
                if room_label in [1041]:
                    roomnums = ["108"]
            elif self.building == "0696" and self.floornum == "3":
                roomnums = re.findall("3[0-9][0-9]?", text)
                if room_label in [216]:
                    roomnums = ["301"]
                if room_label in [241,296]:
                    roomnums = ["303"]
                if room_label in [445]:
                    roomnums = ["305"]
                if room_label in [213,335]:
                    roomnums = ["302"]
                if room_label in [363]:
                    roomnums = ["306"]
                if room_label in [446]:
                    roomnums = ["308"]
            elif self.building == "0703" and self.floornum == "1":
                roomnums =  re.findall("1[0-9][0-9]", text)
                if room_label == 318:
                    roomnums = ["114"]
            elif self.building == "0703" and self.floornum == "3":
                roomnums =  re.findall("3[0-9][0-9]", text)
                if room_label in [52,35,64,124]:
                    roomnums = ["312"]
                if room_label in [331]:
                    roomnums = ["316"]
            elif efr or self.building == "0056":
                roomnums = re.findall("[0-9]" + self.floornum + "[0-9]", text)
            elif two_digit:
                roomnums = re.findall("[0-9][0-9][0-9]?", text)
            else:
                roomnums = re.findall(self.floornum + "[0-9][0-9]", text)
            if roomnums != [] and roomnums[0] != "00":
                self.rooms[room_label] = Room(rooms, room_label, roomnums[0], self.building)
            # elif len(text) > 0:
            #     print text
    def find_doors(self, cluttered, close_door, corr_thresh = .025):
        rdfs = ("door3.png", "slant.png", "halfdoor.png")
        ref_doors = [find_border(cv.imread(f, cv.IMREAD_GRAYSCALE)) for f in rdfs]
        segments = self.segments
        rooms = segments["rooms"]
        # if verbose:
        #     defect_canvas = cv.cvtColor(np.zeros(rooms.img.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
        for room_label in rooms.labels:
            if room_label == 0: continue # skip the blackness
            if room_label == 231 and self.building == "0627" and self.floornum == "3":
                continue

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
                # check to make sure defect actually touches connected component
                if not any(roomlabels[j,i] == room_label for i,j in [
                        [defect_left+1,defect_bottom-1],
                        [defect_left+1,defect_top+1],
                        [defect_right-1,defect_bottom-1],
                        [defect_right-1,defect_top+1]
                    ]):
                    continue
                defect_cutout = defects.cutout(defect_label)
                contours = find_border(defect_cutout)
                
                correlation = min([cv.matchShapes(ref_door[0], contours[0], 1, 0.0) for ref_door in ref_doors])


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
            local_closing = min(
                closing,
                r_left, r_top,
                self.original.shape[0] - r_bottom,
                self.original.shape[1] - r_left
            )
            cutout = img[r_top-local_closing:r_bottom+local_closing,r_left-local_closing:r_right+local_closing]

            # draw room's convex hull on its own canvas
            room_hull = rooms.convex_hull(door.into)
            room_hull_pic = cv.cvtColor(np.zeros(cutout.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            cv.drawContours(room_hull_pic, room_hull, 0, (255,255,255), thickness=-1, offset=(closing,closing))
            room_hull_pic = cv.cvtColor(room_hull_pic, cv.COLOR_RGB2GRAY)

            # draw door in its own canvas and dilate
            offset = (door.getRelOrigin()[0]+local_closing, door.getRelOrigin()[1]+local_closing)
            door_canvas = cv.cvtColor(np.zeros(cutout.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
            door_canvas = cv.drawContours(door_canvas, door.contours, 0, (255,255,255), thickness=-1, offset =offset)
            door_canvas = cv.cvtColor(door_canvas, cv.COLOR_RGB2GRAY)
            door_canvas = cv.dilate(door_canvas, self.kernel, iterations = closing)

            # take intersection of two
            intersect = cv.bitwise_and(door_canvas, room_hull_pic)

            # update labels
            sublabelled = labelled[r_top-local_closing:r_bottom+local_closing,r_left-local_closing:r_right+local_closing]
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
                "dimensions": self.original.shape[:2],
                "level": self.floornum} for room in self.rooms.values()]
    def draw_doors(self):
        for door in self.doors:
            door.draw(self.original)
    def draw_rooms(self):
        for room in self.rooms.values():
            room.draw(self.original)