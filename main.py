from PIL import ImageGrab, Image
import win32gui
from time import sleep
import cv2 as cv
import imutils
import pytesseract
import numpy as np
import os
import glob
import pyautogui
import keyboard

import windowmanager
import imageprocessing

def reconnect(login):
    windowmanager.leftClick(login)
    sleep(5)

    windowmanager.leftClick((1354, 967))

def check_if_kicked():
    point = (1522, 581)
    size = (60, 27)

    text1 = imageprocessing.get_text(point, size, 1)

    point = (1522, 618)
    size = (60, 27)

    text2 = imageprocessing.get_text(point, size, 1)

    if 'yu' in text1 and 'yu' in text1:
        print('Kicked.')
        return True
    
    print('Not kicked.')
    return False

def revive():
    while check_if_dead():
        windowmanager.leftClick((1041, 376))

def check_if_dead():
    point = (984, 340)
    size = (112, 19)

    text = imageprocessing.get_text(point, size, 1)

    if 'Res' in text:
        print('Dead.')
        return True

    print('Not dead.')
    return False

def restart_here():
    windowmanager.leftClick()

def show_image(image):
    cv.imshow('Result', image)
    cv.waitKey()

def get_hp():
    image = windowmanager.take_screenshot()

    point = (1408, 293)
    size = (36, 17)

    text = imageprocessing.get_text(point, size, 0)

    # Fix imperfections of image_to_string to fit the expected values.
    text = fix_hp(text)

    return text

def fix_hp(hp):
    # Fix imperfections of image_to_string to fit the expected values.
    if hp[:2] == '10':
        if hp[:3] == '100':
            return hp[:3]
        else:
            return hp[:2]
    else:
        return hp[:2]

def get_samples(img_dir):
    # Get sample images from a directory. They will be used to find patterns on the screenshot.
    data_path = os.path.join(img_dir, '*g')
    files = glob.glob(data_path)
    data = []

    for f in files:
        # print(f)
        img = cv.imread(f, cv.TM_CCOEFF)
        data.append(img)

    return data

def show_best_match(image, top_left, needle):
    bottom_right = (top_left[0] + needle[0], top_left[1] + needle[1])

    cv.rectangle(image, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    cv.imshow('Result', image)
    cv.waitKey()

def search_stone(img_dir, image):
    samples = get_samples(img_dir)
    
    min_val = None
    min_loc = (0, 0)

    for s in samples:
        # Match for each sample.
        result = cv.matchTemplate(image, s, cv.TM_SQDIFF_NORMED)

        # Get the most and the least accurate points on the image. In the cv.TM_SQDIFF_NORMED model the whitest points are the most accurate.
        t_min_val, t_max_val, t_min_loc, t_max_loc = cv.minMaxLoc(result)

        # Debug code.
        # print('Best match top left position: ', t_min_loc)
        # print('Best match confidence: ', t_min_val)

        # Find the minimum value (Most accurate on this model).
        if min_val == None or t_min_val < min_val:
            min_val = t_min_val
            min_loc = t_min_loc

            needle_w = s.shape[1]
            needle_h = s.shape[0]

    print('Total best match top left position: ', min_loc)
    print('Total best match confidence: ', min_val) 

    # show_best_match(image, min_loc, (needle_w, needle_h))

    return min_loc, min_val

def go_to_map():
    # Open inventory
    x = 1838
    y = 1019
    windowmanager.leftClick((x, y))

    # Switch to tab 1.
    x = 1765
    y = 670
    windowmanager.rightClick((x, y))
    sleep(0.2)

    # Press the ring.
    x = 1867
    y = 734
    windowmanager.rightClick((x, y))
    sleep(0.2)

    # Select map.
    x = 1405
    y = 685
    windowmanager.leftClick((x, y))
    sleep(0.2)

    # Select area.
    # Left side ork.
    # x = 1408
    # y = 607

    # Right side ork.
    x = 1409
    y = 636
    windowmanager.leftClick((x, y))

def out_of_window(loc):
    x = 895
    y = 270
    w = 1024
    h = 731

    if loc[0] < x or loc[1] < y or loc[0] > x + w or loc[1] > y + h:
        return True
    
    return False

def calibrate_screen():
    print('Calibrating...')

    keyboard.press('f')
    sleep(2)
    keyboard.release('f')
    sleep(0.1)

    keyboard.press('t')
    sleep(4)
    keyboard.release('t')
    sleep(0.1)

    keyboard.press('f')
    sleep(2)
    keyboard.release('f')
    sleep(0.1)

    # keyboard.press('e')
    # sleep(5)
    # keyboard.release('e')
    # sleep(0.1)

    keyboard.press('g')
    sleep(0.1)
    keyboard.release('g')
    sleep(0.1)

    keyboard.press('f')
    sleep(2)
    keyboard.release('f')
    sleep(0.1)

    print('Calibration done.')

def search(sample_dir):
    windowmanager.press_button('e', 1)
    image = windowmanager.take_screenshot()
    print('Searching for stone...')
    loc, val = search_stone(sample_dir, image)

    if not out_of_window(loc) and val < 0.07:
        print('Stone found.')
        windowmanager.leftClick(loc)
        return True
    else:
        print('Stone not found.')
        return False

client = []
login = []
sample_dir = "samples\\"

# for i in range(0, client_num):
#     client.append((windowmanager.get_window_position(), windowmanager.get_window_centre()))

client.append(((182, 1064), (1420, 694)))
client.append(((336, 1064), (1420, 694)))
client.append(((508, 1064), (1420, 694)))
client.append(((679, 1064), (1420, 694)))

login.append((1590, 594))
login.append((1590, 625))
login.append((1590, 671))
login.append((1590, 704))

same_hp = []
prev_hp = []
just_joined = []
just_joined2 = []
not_found = []

for i in client:
    same_hp.append(0)
    prev_hp.append(101)
    just_joined.append(False)
    just_joined2.append(False)
    not_found.append(0)

i = 0

loop = 0

i = 0

while True:
    windowmanager.leftClick(client[i][0])
    print('\nLoop:', loop)
    print('Player', i)

    if just_joined[i]:
        calibrate_screen()
        just_joined[i] = False

    if just_joined2[i]:
        go_to_map()
        just_joined2[i] = False
        just_joined[i] = True

    if check_if_kicked():
        just_joined2[i] = True
        reconnect(login[i])
    elif check_if_dead():
        just_joined2[i] = True
        revive()
    else:
        windowmanager.press_button('z', 0.1)

        image = windowmanager.take_screenshot()

        if prev_hp[i] == 101:
            if not search(sample_dir):
                 not_found[i] += 1
            else:
                not_found[i] = 0

        hp = get_hp()

        print('Stone HP:', hp)

        if hp == prev_hp[i]:
            same_hp[i] += 1
        else:
            same_hp[i] = 0
        
        prev_hp[i] = hp

        if same_hp[i] >= 1:
            print('Finished.')
            if not search(sample_dir):
                not_found[i] += 1
            else:
                not_found[i] = 0

            same_hp[i] = 0

        windowmanager.press_button('z', 0.1)

    loop += 1

    if not_found[i] > 0:
        print('Stone not found', not_found[i], 'consecutive times.')

    if not_found[i] >= 3:
        print('Reseting.')
        not_found[i] = 0
        just_joined2[i] = True

    if i < len(client) - 1:
        i += 1
    else:
        i = 0
        