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
    WHITE = (255,255,255)
    REDRAW_COLOR = (15*16+15,7*16+11,0)
    BLACK = (0,0,0)
    img = imread(fn, IMREAD_GRAYSCALE)
    colored = cvtColor(img, COLOR_GRAY2RGB)
    colored[img > 0] = WHITE
    colored[img == 0] = REDRAW_COLOR

    imwrite(outFilename, colored)