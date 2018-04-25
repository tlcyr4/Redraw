import cv2 as cv
import numpy as np

from shortcuts import *


class Segment(object):
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
    def cutout(self, label):
        """ Highlight the selected label in white inside an image of its bound"""
        left,right,top,bottom = self.bbox(label)
        cutout = np.copy(self.img[top:bottom,left:right])
        sublabelled = self.labelled[top:bottom, left:right]
        cutout[sublabelled != label] = 0
        return cutout 
    def convex_hull(self, label):
        cutout = self.cutout(label)
        contours = find_border(cutout)
        return [cv.convexHull(contours[0])]
    def colored(self):
        canvas = cv.cvtColor(np.zeros(self.img.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
        for label in self.labels:
            if label != 0:
                canvas[self.labelled == label] = randColor()
                centroid = (int(self.centroids[label][0]), int(self.centroids[label][1]))
                cv.putText(canvas, str(label), centroid, cv.FONT_HERSHEY_TRIPLEX, 3, (10,10,10), thickness = 3) 
        return canvas