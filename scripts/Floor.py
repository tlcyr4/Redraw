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

        if self.building in ["0040","0053"] and self.floornum == "A":
            self.floornum = "0"
        regexes = {
            "0095": "[0-9][0-9][0-9]",
            "0030": {"A": "[0-9]0[0-9]"},
            "0040": {"A": "[0-9]0[0-9]"},
            "0053": {"A": "[0-9]0[0-9]"},
            "0012": "[0-9][0-9][0-9][NS]?",
            "0019": {
                "A": "[B8][0-9][0-4]",
                "1":"[1"+self.floornum +"][0-9][0-9]|[1-9AT][0-9]",
                "2": "1?A?[0-9][0-9]",
                "3":"[1"+self.floornum +"][0-9][0-9]|[1-9AT][0-9]",
                "4":"T[0-9]"
            },
            "0021": {"0":"A[0-9][0-9]"},
            "0023": "[" + self.floornum + "]?[0-9][0-9]|T[01][0-9]",
            "0026": {"3":"[0-9]..?.?[ABC]","1":"["+self.floornum +"][0-9][0-9]|[1-9][0-9][AB]?","2":"["+self.floornum +"][0-9][0-9]|0?[1-9][0-9][AB]?","A":"["+self.floornum +"][0-9][0-9]|[1-9][0-9][AB]?"},
            "0028": {"3":"1[0-4][0-9]|[2-9][0-9]"},
            "0040":"[0-9]" + self.floornum + "[0-9]A?",
            "0042":"[0-9]" + self.floornum + "[0-9]A?",
            "0043":"[0-9]" + self.floornum + "[0-9]A?",
            "0047":"[0-9]" + self.floornum + "[0-9]A?",
            "0049":"[0-9]" + self.floornum + "[0-9]A?",
            "0053":"[0-9]" + self.floornum + "[0-9]A?",
            "0092": {"1":"[0-9]" + self.floornum + "[0-9]"},
            "0148": {"A": "0[0-9][0-9]"},
            "0619": {"1":"T?[0-9][0-9]","2":"T?[0-9][0-9]"},
            "0631": {"A": "B?[0-9][0-9]","2":"[0-9][0-9]|T[0-9]"},
            "0672": self.floornum+"[01][0-9][ABCD]?"
        }
        if self.building in ["0040","0053"] and self.floornum == "0":
            self.floornum = "A"
        skips = {
            "0012": {
                "1": [79],
            },
            "0014": {
                "2": [110],
                "3": [113],
                "4": [123]
            },
            "0021": {
                "0": [803],
                "2": [1]
            },
            "0023": {
                "0": [626],
                "2": [405],
                "3": [500]
            },
            "0028": {"3":[1402]},
            "0148": {"1":[521,746],"2":[158,670],"3":[827,329,99]},
            "0592": {"2":[349]},
            "0631": {"2":[2]},
            "0686": {"3":[19]},
            "0693": {"1":[129],"2":[126]},
            "0694": {"2":[1],"3":[1]},
            "0696": {"1":[458],"2":[279],"3":[144],"4":[24,104]}
        }
        overrides = {
            "0021": {"1": {1493:"111"}},
            "0028": {"1":{237:"111",238:"111"},   "3": {145:"116"}},
            "0043": {"0": {23:"104"}},
            "0092": {"1": {30:"112",67:"113",102:"114"}},
            "0603": {"1":{822:"101",823:"101",1166:"122",1224:"122",1423:"122"},
            "2":{1044:"201",1045:"201", 44:"272",58:"272",103:"272",1535:"222",1660:"222",1522:"202",1725:"202",1751:"202"},
            "3":{1330:"301",1331:"301",1810:"322",1951:"322"}},
            "0631": {"A":{222:"B21"}},
            "0668": {"0":{383:"027"},"3":{25:"301",26:"301",29:"301",33:"301",35:"301",41:"302",46:"302"}},
            "0686": {"4":{22:"402",57:"402",128:"402",129:"404",130:"406",34:"401"}},
            "0693": {"1":{185:"103",215:"103",186:"103",62:"102",63:"102",64:"102",74:"102",188:"105",190:"107",292:"113",316:"113",372:"315",384:"315"},
            "2":{208:"203",182:"203",183:"205",257:"311",314:"311",164:"306"}},
            "0694": {"2":{268:"211",269:"211",271:"211",265:"213",284:"213",512:"214",514:"214",547:"214",510:"216",518:"210"},
                "3": {38:"302",129:"302",139:"302",207:"302",211:"303",225:"304",244:"305",272:"313",273:"313",335:"313",328:"309",334:"309",567:"310"}},
            "0695": {"1": {3:"104",7:"104",14:"104",37:"104",50:"102",60:"102",68:"102",97:"102",51:"101",59:"101",67:"101",137:"101"}},
            "0696": {"1":{727:"104"},"2":{460:"201",769:"205",982:"205",985:"208"},
            "3": {216:"301",241:"303",296:"303",445:"305",213:"302",336:"305",335:"302",363:"306",446:"308"},"4":{318:"406"}},
            "0703": {"1":{318:"114"},"3":{35:"312",52:"312",64:"312",124:"312",331:"316"}}
        }
        replacements = [
                ("O","0"),
                ("I","1"),
                ("Z","2"),
                ("1 1","11")
        ]
        extra_replacements = {
            "0012": [("8","S")],
            "0148": {"3":[("35","36")]},
            "0019": {"4":[("S","6")],"2":[("A2","A02")]},
            "0026": {"2": [("528","052B"),("52A","052A")]},
            "0631": {"A":[("8","B")]},
            "0672": [("8","B"),("GB","G3"),("0B","03")]
        }

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
            if self.building in extra_replacements:
                if self.floornum in extra_replacements[self.building]:
                    replacements += extra_replacements[self.building][self.floornum]
                else:
                    replacements += [tup for tup in extra_replacements[self.building] if type(tup) is tuple]
            for replacee,replacement in replacements:
                text = text.replace(replacee,replacement)
            if self.building in skips:
                if self.floornum in skips[self.building]:
                    if room_label in skips[self.building][self.floornum]:
                        continue
            
            regex = None

            if self.building in regexes:
                if type(regexes[self.building]) is dict and self.floornum in regexes[self.building]:
                    regex = regexes[self.building][self.floornum]
                if type(regexes[self.building]) is str:
                    regex = regexes[self.building]

            if regex != None:
                pass
            elif efr or self.building == "0056":
                regex = "[0-9]" + self.floornum + "[0-9]"
            elif two_digit:
                regex = "[0-9][0-9][0-9]?"
            else:
                regex = self.floornum + "[0-9][0-9]"
            roomnums = re.findall(regex,text)

            if self.building == "0019" and self.floornum == "A":
                if roomnums != [] and roomnums[0][0] == "8":
                    roomnums[0] = "B" + roomnums[0][1:]
            elif self.building == "0026":
                if self.floornum == "3":
                    if roomnums == []:
                        continue
                    roomnums[0] = re.sub(r'\W+', '', roomnums[0])
                    roomnums[0] = "00" + roomnums[0][:2]
            elif self.building == "0631" and self.floornum == "A":
                if roomnums != [] and len(roomnums[0]) < 3:
                    roomnums[0] = "B" + roomnums[0]
            elif self.building == "0631" and self.floornum == "2":
                if roomnums != [] and roomnums[0][0] == "T":
                    roomnums[0] = "T02"
            

            if self.building in overrides:
                if self.floornum in overrides[self.building]:
                    if room_label in overrides[self.building][self.floornum]:
                        roomnums = [overrides[self.building][self.floornum][room_label]]
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
        if self.building in ["0021","0056"] and self.floornum == "0":
            self.floornum = "A"
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
            room.drawOutline(self.original)
        for room in self.rooms.values():
            room.drawNumber(self.original)