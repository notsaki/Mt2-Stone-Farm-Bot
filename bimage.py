from PIL import ImageGrab, Image
import cv2 as cv
import imutils
import pytesseract
import numpy as np

import binput
import bmath
import bfile

def draw_box(image, needles, size):
    top_left = (needles[0], size[1] - needles[1])
    bottom_right = (needles[2], size[1] - needles[3])
    cv.rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    return image

def show_image(image):
    cv.imshow('Result', image)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    cv.waitKey()

def get_text(point=(0, 0), size=(0, 0), pars=None):
    image = binput.take_screenshot()

    # Get stone's HP from the image.
    image = crop_image(image, point, size)

    # show_image(image)

    # Grey scale, rescale, negative and increase of contrast to increase accuracy.
    image = preproc(image)

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Get text from the image.
    text = pytesseract.image_to_string(image, lang='eng', config=pars)
    
    # show_image(image)

    return text

def crop_image(image, top_left, size):
    image = image[top_left[1]: top_left[1] + size[1], top_left[0]: top_left[0] + size[0]]

    return image

def show_best_match(image, top_left, needle):
    bottom_right = (top_left[0] + needle[0], top_left[1] + needle[1])

    cv.rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    show_image(image)

def search_object(dir='', name='', method=cv.TM_SQDIFF_NORMED, hl=0, threshold=0, top_left=None, size=None):
    image = binput.take_screenshot()
    image = crop_image(image, top_left, size)
    # show_image(image)
    samples = bfile.get_images(dir, name)
    
    val = None
    loc = (0, 0)

    for s in samples:
        # Match for each sample.
        result = cv.matchTemplate(image, s, method)

        # show_image(result)

        # Get the most and the least accurate points on the image. Whitest of blackest.
        t_min_val, t_max_val, t_min_loc, t_max_loc = cv.minMaxLoc(result)

        # Find best value.
        if hl == 0:
            if val == None or t_min_val < val:
                val = t_min_val
                loc = t_min_loc

                needle_h = s.shape[0]
                needle_w = s.shape[1]
        else:
            if val == None or t_max_val > val:
                val = t_max_val
                loc = t_max_loc
                
                needle_h = s.shape[0]
                needle_w = s.shape[1]

    needle = (needle_w, needle_h)

    # show_best_match(image, loc, needle)
    # print('Total best match top left position:', loc)
    # print('Total best match confidence:', val)

    loc = bmath.find_centre(loc, needle)

    # Threshold.
    if not threshold == None:
        if hl == 0:
            if val > threshold:
                return None
        else:
            if val <= threshold:
                return None

    return loc
# while True:
#     loc = search_object(dir='icons\\', 
#                     name='inventory_button', 
#                     method=cv.TM_CCORR_NORMED, 
#                     hl=0, 
#                     threshold=20,
#                     top_left=(895, 270),
#                     size=(1024, 600))

def search_all(dir='', name='', method=cv.TM_SQDIFF_NORMED, hl=0, threshold=0, top_left=None, size=None):
    image = binput.take_screenshot()
    image = crop_image(image, top_left, size)

    samples = bfile.get_images(dir, name)

    locations = []
    for s in samples:
        # Match for each sample.
        result = cv.matchTemplate(image, s, method)

        if hl == 0:
           loc = np.where(result <= threshold)
        else:
            loc = np.where(result > threshold)

        loc = list(zip(*loc[::-1]))
        locations += loc

    return locations


def preproc(image):
    # Resize
    image = imutils.resize(image, width=500)

    # Greyscale.
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Threshold.
    image = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    return image