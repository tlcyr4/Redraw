from cv2 import imread, imwrite, IMREAD_COLOR
from glob import glob
import sys
from os import path
import numpy as np

inFiles = glob(sys.argv[1])
for fn in inFiles:
    print fn
    outFilename = path.join(".", "jpg", path.basename(fn))
    outFilename = outFilename[:-3] + "jpg"
    # COLOR = (10*16+11,4*16+8,0)
    img = imread(fn, IMREAD_COLOR)
    # colored = cvtColor(img, COLOR_GRAY2RGB)
    # colored[img > 0] = COLOR

    imwrite(outFilename, img)