import cv2 as cv
from glob import glob
import sys
from os import path
import numpy as np

from Segment import Segment
from shortcuts import *

inFiles = glob(sys.argv[1])
for fn in inFiles:
    print fn
    outFilename = path.join(".", "preprocessed", path.basename(fn))
    img = cv.imread(fn, cv.IMREAD_GRAYSCALE)
    # original = np.copy(img)
    img = (255-img)
    if "0694-00" in fn or "0696-00" in fn or "0696-01" in fn or "0696-02" in fn or "0047-00" in fn or "0060-01" in fn:
        img = cv.threshold(img, 1, 255, cv.THRESH_BINARY)[1]
    elif "0053-01" in fn or "0053-02" in fn:
        img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)[1]
    else:
        img = cv.threshold(img, 200, 255, cv.THRESH_BINARY)[1]
    thresholded = np.copy(img)
        

    if len(img) > len(img[0]): 
        img[:,6255:] = 0
    num_ccs, labelled, stats, centroids = cv.connectedComponentsWithStats(img)
    numBorders = 2
    altBorders = {
        "0148-01":1,
        "0592-01":1,
        "0592-02":1,
        "0592-03":1,
        "0592-04":1,
        "0056":1,
        "1901":1,
        "1903":1,
        "Alexander":1,
        "Pyne":1,
        "Lockhart":1,
        "0060-0":1,
    }
    for nb in altBorders:
        if nb in fn:
            numBorders = altBorders[nb]
    stats[:numBorders+1,cv.CC_STAT_AREA] = 0

    
    ccs = {
        "0014-01":[1,2],
        "0673-02":[1,2],
        "0636-00":[1,3],
        "0686-04":[2,3],
        "0672-04":[2],
        "0674-02":[2],
        "0021-05":[2],
        "0028-01":[1,2],
        "0148-01":[1],
        "0071-01":[1,2,4],
        "0694-01":[1,2],
        "0627-01":[1,2],
        "0627-02":[1,2],
        "0694-00":[1],
        "0695-00":[1,3],
        "0695-01":[1,3],
        "0696-03":[1,3],
        "0693-01":[1,2],
        "0153-01":[1,2,3,4,5,7,8,9],
        "0153-02":range(1,8),
        "0153-03":[1,2],
        "0148-04":[1,3],
        "0047-04":[1,2],
        "0030-A":[1,2],
        "0668-04":[1,2],
        "0043-05":[2],
        "0042-04":[2],
        "0023-01":[1,2],
        "0040-01":[1,2,3],
        "0603-01":[1,2,3,4],
        "0603-02":[1,2],
        "0153-04":[1,3],
        "0153-A":[1,2],
        "0619-01":[1,2]
    }
    cclist = [1]
    for cc in ccs:
        if cc in fn:
            cclist = ccs[cc]
    areas = sorted(stats[:, cv.CC_STAT_AREA])[::-1]
    
    

    img[:,:] = 0
    for i in cclist:
        img[stats[labelled, cv.CC_STAT_AREA] == areas[i-1]] = 255

    if "-clean" in sys.argv:
        cv.imwrite(outFilename, img)
        exit()
    segment = Segment(img)
    hulls = [segment.convex_hull(cc) for cc in range(1,1+len(cclist))]
    origins = (Point(segment.bbox(cc)[0::2]) for cc in range(1,1+len(cclist)))

    segment = Segment(img)
    bboxes = [segment.bbox(label) for label in segment.labels if label != 0]
    left = min(bbox[0] for bbox in bboxes)
    right = max(bbox[1] for bbox in bboxes)
    top = min(bbox[2] for bbox in bboxes)
    bottom = max(bbox[3] for bbox in bboxes)

    bbox = (left,right,top,bottom)

    # bring back things inside convex hull

    mask = cv.cvtColor(np.zeros(img.shape, dtype="uint8"), cv.COLOR_GRAY2RGB)
    [cv.drawContours(mask, hull, 0, WHITE, thickness = -1, offset=origins.next()) for hull in hulls]
    mask = cv.cvtColor(mask, cv.COLOR_RGB2GRAY)
            
    img = cv.bitwise_and(thresholded, mask)

    if "-trim" in sys.argv:
        img = img[top:bottom,left:right]
    


    
    cv.imwrite(outFilename, img)