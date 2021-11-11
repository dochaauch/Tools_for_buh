from icecream import ic
from datetime import datetime
import time
import os
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re

def time_format():
    return f'{datetime.now()}|> '


ic.configureOutput(prefix=time_format, includeContext=True)

pdfs = glob.glob(r'/Users/docha/Google Диск/Bonus/2021-05/*.pdf')


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction поворот изображения
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


def show_image(img, **kwargs):
    """
    Show an RGB numpy array of an image without any interpolation
    """
    plt.subplot()
    plt.axis('off')
    plt.imshow(
        X=img,
        interpolation='none',
        **kwargs
    )


def my_str_to_float(str):
    # str '13,50' => float '13.5'
    return float(str.replace(',', '.'))


def my_short_date(str):
    # '21.05.2021' => '21.05.21'
    return str[:6] + str[-2:]

arve_content = dict()
#filePath = '/Users/docha/Google Диск/Bonus/2021-04/a22_29.04.2021_bonus_tolkeburoo_waved_stripes.pdf'
for filePath in pdfs:

    doc = convert_from_path(filePath)
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)
    #ic(doc, path, fileBaseName, fileExtension)

    r1 = re.compile(r'^\d{6}.*$')
    if not r1.search(fileBaseName.lower()):  # не начинается с 6 цифр и что-то еще, чтобы
                                                # исключить исходящие счета

        for page_number, page_data in enumerate(doc):
            page_data.hasAlphaChannel = lambda: False
            custom_config = r'-l "est+rus" --oem 3 --psm 1'
            pil_image = Image.fromqimage(page_data)
            open_cv_image = np.array(pil_image)
            img = open_cv_image[:, :, ::-1].copy()

            gray = get_grayscale(img)
            thresh = thresholding(gray)
            #cv2.imshow('ImageWindow', img)
            #cv2.waitKey(0)
            #opening = opening(gray)
            #canny = canny(gray)
            txt = pytesseract.image_to_string(img, config=custom_config)
            txt = re.sub(r'\s+', ' ', txt)
            #print("Page # {} - {}".format(str(page_number), txt))
            arve_content[fileBaseName] = txt

arve = dict()
ic(arve_content)

#"01.05.21","31.05.21","6P"
#"Subconto", "6:144","Armina  OU",,"15:1", "91:0"
#"Subconto", "6:144:1","2021",,
#"Subconto", "6:144:1:2","210531 1953",,"15:1","20:20.16","21:07.06.21","23:0","25:1953","26:31.05.21","30:31.05.21"
#"6P","31.05.21","68","1","60","1","3.36","HAE. 21018 : KM Armina OU :","15:11","6:144:1:2","","",""
#"6P","31.05.21","26","","60","1","16.80","HAE. 21018 : Armina OU :","8:6:31","6:144:1:2","1.000","",""

for k, v in arve_content.items():
    if 'Armina' in v:
        nimi = 'Armina'
        reg_digits_coma = r'(\b\d+,\d{2}\b)'
        reg_date = r'(\b\d+.\d+.\d+\b)'
        #tx = r'Summa km-ta 20% (\b\d+,\d{2}\b)'
        list_find_sum = [r'Summa km-ta 20% ', r'Käibemaks 20% ', r'Arve kokku \(EUR\) ']
        list_find_sum_res = []
        for l in list_find_sum:
            list_find_sum_res.append(my_str_to_float(re.findall(l+reg_digits_coma, v)[0]))
        ic(list_find_sum_res)
        #list_find_date = [r'Kuupäev ', r'Maksetähtpäev ']
        tx = tx1 + reg_digits_coma
        ic(tx)
        summa_kta = my_str_to_float(re.findall(tx, v)[0])
        #summa_kta = my_str_to_float(re.findall(r'Summa km-ta 20% (\b\d+,\d{2}\b)', v)[0])
        km = my_str_to_float(re.findall(r'Käibemaks 20% (\b\d+,\d{2}\b)', v)[0])
        summa = my_str_to_float(re.findall(r'Arve kokku \(EUR\) (\b\d+,\d{2}\b)', v)[0])
        arve = re.findall(r'Arve nr (\b\d+\b)', v)[0]
        kuupaev = my_short_date(re.findall(r'Kuupäev ', v)[0])
        tahtaeg = my_short_date(re.findall(r'Maksetähtpäev (\b\d+.\d+.\d+\b)', v)[0])
        ic(nimi, summa_kta, km, summa, arve, kuupaev, tahtaeg)

    if 'OCULUS' in v:
        nimi = 'Oculus'
        summa_kta = my_str_to_float(re.findall(r'Summa ilma käibemaksuta (\b\d+,\d{2}\b)', v)[0])
        km = my_str_to_float(re.findall(r'Käibemaks 20% (\b\d+,\d{2}\b)', v)[0])
        summa = my_str_to_float(re.findall(r'Tasumisele kuulub (\b\d+,\d{2}\b)', v)[0])
        arve = re.findall(r'ARVE NR (\b\d+\b)', v)[0]
        kuupaev = my_short_date(re.findall(r'Kuupäev: (\b\d+.\d+.\d+\b)', v)[0])
        tahtaeg = my_short_date(re.findall(r'tähtpäev: (\b\d+.\d+.\d+\b)', v)[0])
        ic(nimi, summa_kta, km, summa, arve, kuupaev, tahtaeg)
