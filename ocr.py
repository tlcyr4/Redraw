from pytesseract import pytesseract as pt
from PIL import Image
import os
import sys
import re

img = Image.open(sys.argv[1])

os.environ["TESSDATA_PREFIX"] = ".\\"

output = pt.image_to_string(img).encode("utf-8").strip()

print re.findall("[0-6][0-9][0-9]", output) # First digit is floor number

# f = open(sys.argv[2], "w")

# f.write(output)
# f.write('\n')
# f.close()