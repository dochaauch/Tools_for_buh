from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

PDF_file = "/Users/docha/Google Диск/Bonus/2021-04/a22_29.04.2021_bonus_tolkeburoo_waved_stripes.pdf"

pages = convert_from_path(PDF_file, 500)

image_counter = 1

for page in pages:
    filename = "page_" + str(image_counter) + ".jpg"
    page.save(filename, 'JPEG')
    image_counter = image_counter + 1

filelimit = image_counter - 1

outfile = "out_text.txt"

f = open(outfile, "w")

for i in range(1, filelimit + 1):
    filename = "page_" + str(i) + ".jpg"
    custom_config = r'-l "est+rus" --oem 0 --psm 1 boxes=True'
    text = str((pytesseract.image_to_string(Image.open(filename), config=custom_config)))
    text = text.replace('-\n', '')
    f.write(text)

f.close()