import random

import cv2 as cv 
RED = (0,0,255)
GREEN = (0,255,0)
BLUE = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PRINCETON_ORANGE = (37,128,245)

def randColor():
    """ return a random but bright BGR color """
    return tuple(random.sample(xrange(128,256),3))

def find_border(img):
    return cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]

def Point(coords):
    return tuple(map(int, coords))