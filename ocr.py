from pytesseract import pytesseract as pt
from PIL import Image
import os

img = Image.open("temp.png")

os.environ["TESSDATA_PREFIX"] = ".\\"

os.system("tesseract test.png result hocr")

# os.system("tesseract --print-parameters > params.txt")

# boxes = pt.run_tesseract('temp.png', 'output', "box", "eng")

# boxes = pt.image_to_boxes(img)