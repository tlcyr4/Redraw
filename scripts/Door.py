import cv2 as cv


from shortcuts import *

class Door:
    def __init__(self, bbox, contours, outof, into, rel_origin):
        self.bbox = bbox
        self.contours = contours
        self.outof = outof
        self.into = into
        self.origin = (bbox[0],bbox[2])
        self.rel_origin = rel_origin
    def getRelOrigin(self):
        """ Get door's origin relative to the origin of the room it's in """
        return self.rel_origin
    def draw(self, img, color = GREEN):
        cv.drawContours(img, self.contours, 0, color, thickness = -1, offset = self.origin)