from cv2 import imread, imwrite, IMREAD_GRAYSCALE
from glob import glob
import sys
from os import path
import numpy as np

inFiles = glob(sys.argv[1])
for fn in inFiles:
    print fn
    outFilename = path.join(".", "shrunk", path.basename(fn))
    # outFilename = outFilename[:-3] + "jpg"
    img = imread(fn, IMREAD_GRAYSCALE)
    # shrink
    scaleFactor = 10
    mini = np.zeros((img.shape[0]/scaleFactor,img.shape[1]/scaleFactor),np.uint8)
    # minic=np.indices((img.shape[0]/scaleFactor,img.shape[1]/scaleFactor)).swapaxes(0,2).swapaxes(0,1)
    # minix = arange(mini.shape[1])
    # miniy = arange(mini.shape[0])
    # mini[img[minic*scaleFactor:minic*scaleFactor+scaleFactor,minic*scaleFactor:minic*scaleFactor+scaleFactor]] = 255
    # mini[any(img)]
    for y in xrange(len(mini)):
        for x in xrange(len(mini[0])):
            if np.any(img[y*scaleFactor:y*scaleFactor+scaleFactor,x*scaleFactor:x*scaleFactor+scaleFactor] == 255):
                mini[y,x] = 255

    imwrite(outFilename, mini)