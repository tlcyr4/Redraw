import cv2 as cv

from shortcuts import *

class Room:
    def __init__(self, segment, label, number, building):
        self.label = label
        self.number = number
        self.segment = segment
        cutout = segment.cutout(label)
        self.contours = find_border(cutout)
        self.poly = cv.approxPolyDP(self.contours[0], 10, True)
        self.building = building
    def getCentroid(self):
        centroid = self.segment.centroids[self.label]
        return (int(centroid[0]),int(centroid[1]))
    def getArea(self):
        return self.segment.stats[self.label, cv.CC_STAT_AREA]
    def getBbox(self):
        return self.segment.bbox(self.label)
    def getOrigin(self):
        bbox = self.getBbox()
        return (bbox[0],bbox[2])
    def getPoly(self):
        return self.poly
    def draw(self, img, color = RED):
        cv.drawContours(img, [self.getPoly()], 0, color, thickness = 5, offset = self.getOrigin())
        centroid = self.getCentroid()
        cv.putText(img, self.number, centroid, cv.FONT_HERSHEY_TRIPLEX, 3, BLUE, thickness = 3)    