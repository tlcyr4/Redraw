import cv2 as cv
from glob import glob
import sys
from os import path
import numpy as np

inFiles = glob(sys.argv[1])
for fn in inFiles:
    print fn
    outFilename = path.join(".", "preprocessed", path.basename(fn))
    img = cv.imread(fn, cv.IMREAD_GRAYSCALE)
    grays = ["0696-00","0696-01","0696-02","0694-00"]
    isgray = False
    for r in grays:
        if r in fn:
            isgray = True
    img = (255-img)
    if isgray:
        pass
        # img = cv.threshold(img, 150, 255, cv.THRESH_BINARY)[1]
    else:
        img = cv.threshold(img, 200, 255, cv.THRESH_BINARY)[1]
        

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
        "0696-00":5,
        "1901":1,
        "1903":1,
        "Alexander":1,
        "Pyne":1,
        "Lockhart":1,
        "0060-0":1
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
        "0694-00":range(1,20),
        # "0696-01":range(1,10),
        # "0696-02":range(1,10),
        "0153-01":[1,2,3,4,5,7,8],
        "0153-02":range(1,8),
        "0043-05":[2],
        "0042-04":[2]
    }
    cclist = [1]
    for cc in ccs:
        if cc in fn:
            cclist = ccs[cc]
    areas = sorted(stats[:, cv.CC_STAT_AREA])[::-1]
    img[:,:] = 0
    for i in cclist:
        img[stats[labelled, cv.CC_STAT_AREA] == areas[i-1]] = 255

    


    
    cv.imwrite(outFilename, img)