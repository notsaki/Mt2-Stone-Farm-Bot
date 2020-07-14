from PIL import ImageGrab, Image
import cv2 as cv
import imutils
import pytesseract
import numpy as np
import os

import binput
import bmath
import bfile
import re 

def draw_box(image, needles, size):
    top_left = (needles[0], size[1] - needles[1])
    bottom_right = (needles[2], size[1] - needles[3])
    cv.rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    return image

def show_image(image):
    cv.imshow('Result', image)
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

# def find_text(text='', top_left=None, size=None):
#     image = binput.take_screenshot()
#     image = crop_image(image, top_left, size)
#     size = (size[0] * 6, size[1] * 6)
#     image = imutils.resize(image, width=size[0])

#     pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#     loc = pytesseract.image_to_boxes(image)
    
#     # text = ''
#     for i in loc.splitlines():
#     #     text += i[0]
#         l = i.split(' ')
#         # x, y, w, h = int(l[1]), int(l[2]), int(l[3]), int(l[4])
#         # image = draw_box(image, (x, y, w, h), size)

#     image = imutils.resize(image, width=1024)

#     index = loc[0].find('MetinofShadow')
#     text = list(zip(*text))

#     # Loop.
#     l = loc[index].split(' ')
#     x, y, w, h = int(loc[index][1]), int(loc[index][2]), int(loc[index][3]), int(loc[index][4])
#     image = draw_box(image, (x, y, w, h), size)

#     show_image(image)

def crop_image(image, top_left, size):
    image = image[top_left[1]: top_left[1] + int(size[1]), top_left[0]: top_left[0] + int(size[0])]

    return image

def show_best_match(image, top_left, needle):
    bottom_right = (top_left[0] + needle[0], top_left[1] + needle[1])

    cv.rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    show_image(image)

def search_object(dir='', name='', method=cv.TM_SQDIFF_NORMED, hl=0, threshold=0, top_left=None, size=None):
    image = binput.take_screenshot()
    image = crop_image(image, top_left, size)

    samples = bfile.get_images(dir, name)
    
    val = None
    loc = (0, 0)

    for s in samples:
        # Match for each sample.
        result = cv.matchTemplate(image, s, method)

        # if name == 'teleport_ring':
        #     show_image(result)
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

    # if name == 'teleport_ring':
    #     show_best_match(image, loc, needle)
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

    # print(locations)

    return locations


def preproc(image):
    # Resize
    image = imutils.resize(image, width=500)

    # Greyscale.
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Threshold.
    image = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

    return image

# loc = search_all(dir='stones\\city2\\',
#     method=cv.TM_SQDIFF_NORMED, 
#     hl=0, 
#     threshold=0.1,
#     top_left=(895, 270),
#     size=(1024, 731))

# c = bmath.find_closest(bmath.find_centre((895, 270), (1024, 731)), loc)
# print(c)
# find_text(text='Metin of Shadow', 
#         top_left=(1, 31), 
#         size=(1024, 731))

# def get_hp(dir='', name='', method=cv.TM_SQDIFF_NORMED, hl=0, threshold=0, top_left=None, size=None):
#     image = binput.take_screenshot()
#     image = crop_image(image, top_left, size)

#     samples = bfile.get_images(dir, name)
#     files = bfile.get_files(dir)[::-1]

#     val = None
#     loc = (0, 0)
#     s_max = None

#     for i in range(0, len(samples)):
#         # Match for each sample.
#         result = cv.matchTemplate(image, samples[i], method)

#         # if name == 'teleport_ring':
#         #     show_image(result)
#         # show_image(result)

#         # Get the most and the least accurate points on the image. Whitest of blackest.
#         t_min_val, t_max_val, t_min_loc, t_max_loc = cv.minMaxLoc(result)
#         if t_min_val > threshold:
#             print(files[i])
#             hp = re.findall(r'\d+', files[i])
#             hp = bmath.to_int(hp)

#             print('Total best match confidence:', t_min_val)

#             return hp

#     return 0

# def fix_hp(hp):
#     # Fix imperfections of image_to_string to fit the expected values.
#     if hp[:2] == '10':
#         if hp[:3] == '100':
#             return hp[:3]
#         else:
#             return hp[:2]
#     else:
#         return hp[:2]

# while True:
#     loc = search_object(dir='icons\\hp',
#                 method=cv.TM_SQDIFF_NORMED, 
#                 hl=0, 
#                 threshold=0.4,
#                 top_left=(895, 270),
#                 size=(1024, 731))

#     if loc:
#         print('Found.')

    # if loc:
    #     print('Found.')
    # else:
    #     print('Not found.')