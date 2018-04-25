from cv2 import imread, imwrite, IMREAD_GRAYSCALE, cvtColor, COLOR_GRAY2RGB
from glob import glob
import sys
from os import path
import numpy as np

inFiles = glob(sys.argv[1])
for fn in inFiles:
    print fn
    outFilename = path.join(".", "colored", path.basename(fn))
    # outFilename = outFilename[:-3] + "jpg"
    COLOR = (15*16+15,7*16+11,0)
    img = imread(fn, IMREAD_GRAYSCALE)
    colored = cvtColor(img, COLOR_GRAY2RGB)
    colored[img > 0] = COLOR

    imwrite(outFilename, colored)