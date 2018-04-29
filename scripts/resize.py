from cv2 import imread, imwrite, IMREAD_GRAYSCALE
from glob import glob
import sys
from os import path
import numpy as np

inFiles = glob(sys.argv[1])
for fn in inFiles:
    print fn
    outFilename = path.join(".", "resized", path.basename(fn))
    # outFilename = outFilename[:-3] + "jpg"
    img = imread(fn, IMREAD_GRAYSCALE)
    if "0668-00" in fn:
        img = img[img.shape[0]-6600:,:]
    # shrink
    # goal size is 10200X6600
    new = np.zeros((6600,10200))
    xpad = (10200 - img.shape[1])/2
    ypad = (6600 - img.shape[0]) / 2
    new[ypad:ypad+img.shape[0],xpad:xpad+img.shape[1]] = img

    imwrite(outFilename, new)