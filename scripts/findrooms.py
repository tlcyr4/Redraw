from os import path
import sys
import json
import time
from glob import glob
import winsound
import atexit

import cv2 as cv

from shortcuts import *
from Floor import Floor

def main(inFilename):

    # parse/use inFilename
    img = cv.imread(inFilename, cv.IMREAD_GRAYSCALE)
    print(inFilename)
    outFilename = path.join("data", "polygons", path.basename(inFilename))
    building = path.basename(inFilename)[:4]
    floornum = path.splitext(path.basename(inFilename))[0][-1]

    # get settings for this building
    settings = {}
    for line in open("scripts/settings.txt", "r"):
        tokens = line.split("\t")
        settings[tokens[0].strip(":").lower()] = building in tokens[1:]

    # run analysis
    floor = Floor(cv.imread(inFilename, cv.IMREAD_COLOR), floornum, building, preprocessed=preprocessed)
    text_thresh = 2200
    if building == "0010":
        text_thresh = 3000
    floor.segment(room_upper_thresh = None, text_thresh=text_thresh)
    floor.find_doors(settings["cluttered"], settings["close_door"], corr_thresh = .03)
    floor.transplant_doors()
    floor.find_rooms(settings["efr"], settings["two_digit"])
    
    # draw results
    floor.draw_doors()
    floor.draw_rooms()
    
    # output results
    if not real:
        outFilename = "debug.png"
    jsonFilename = path.splitext(outFilename)[0] + ".json"
    json.dump(floor.toJSON(), open(jsonFilename, "w"))
    cv.imwrite(outFilename, floor.original)
    
    # output extra debugging info
    if mark:
        cv.imwrite(path.join("marked",path.basename(inFilename)), floor.segments["rooms"].colored())
    if verbose:
        cv.imwrite("debug_rooms.png", floor.segments["rooms"].colored())
        cv.imwrite("debug_text.png", floor.segments["text"].img)
        cv.imwrite("debug_no_text.png", floor.segments["no_text"].img)

# ring bell when done
atexit.register(winsound.Beep, 600, 250)

inFiles = glob(sys.argv[1])

# command line options
mark = "-m" in sys.argv
verbose = "-v" in sys.argv
timing = "-time" in sys.argv
real = "-real" in sys.argv
preprocessed = "-p" in sys.argv


if timing:
    totalTime = 0
    missed = 0

for inFilename in inFiles:
    if timing:
        start = time.clock()
    main(inFilename)
    if timing:
        duration = time.clock() - start
        totalTime += duration
        try:
            print "Wall Clock Time: ", duration
        except:
            missed += duration
if timing:
    print "missed: ", missed
    print "total time: ", totalTime
