from PIL import ImageGrab, Image
import win32gui
from time import sleep
import cv2 as cv
import imutils
import pytesseract
import numpy as np

import windowmanager

def get_text(point, size, type):
    image = windowmanager.take_screenshot()

    # Get stone's HP from the image.
    image = crop_image(image, point, size)

    # Grey scale, rescale, negative and increase of contrast to increase accuracy.
    image = preproc(image)

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Get text from the image.
    if type == 0:
        text = pytesseract.image_to_string(image, lang='eng', config='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789%')
    else:
        text = pytesseract.image_to_string(image, lang='eng', config='--psm 8 --oem 1')

    # print(text)
    # cv.imshow('Image', image)
    # cv.waitKey(0)

    return text

def save_image(image):
    image = image[:, :, ::-1].copy()
    image = Image.fromarray(image)
    image.save('screenshots/1.png')

def get_image(h):
    image = windowmanager.take_window_screenshot(bbox)

    # save_image(image)
    # cv.imshow('Image', image)

    # cv.waitKey(0)

    return image

def crop_image(image, point, size):
    # Crop stone life.
    image = image[point[1]:point[1]+size[1], point[0]:point[0]+size[0]]

    return image

def preproc(image):
    # Resize
    image = imutils.resize(image, width=500)
    # Greyscale.
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Threshold.
    image = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    return image