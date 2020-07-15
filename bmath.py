import cv2 as cv
import math

def get_relative(top_left, new_top_left, def_pos):
    dif = (def_pos[0] - top_left[0], def_pos[1] - top_left[1])

    pos = (new_top_left[0] + dif[0], new_top_left[1] + dif[1])

    return pos

def find_centre(top_left, needle):
    x = top_left[0] + (needle[0] / 2)
    y = top_left[1] + (needle[1] / 2)

    return (int(x), int(y))

def to_int(str):
    num = ''

    for i in str:
        if i in '1234567890':
            num += i

    if len(num) < 1:
        return 0

    return int(num)

def get_tuple(str):
    tup = ()
    pos = str.split(',')
    for i in range(0, len(pos)):
        pos[i] = pos[i].strip()

    for i in pos:
        tup += (int(i), )

    return tup

def window_to_full(pos, top_left):
    return (pos[0] + top_left[0], pos[1] + top_left[1])

def method_to_const(method):
    if 'TM_SQDIFF' in method:
        return cv.TM_SQDIFF
    elif 'TM_SQDIFF_NORMED' in method:
        return cv.TM_SQDIFF_NORMED
    elif 'TM_CCORR' in method:
        return cv.TM_CCORR
    elif 'TM_CCORR_NORMED' in method:
        return cv.TM_CCORR_NORMED
    elif 'TM_CCOEFF' in method:
        return cv.TM_CCOEFF
    elif 'TM_CCOEFF_NORMED' in method:
        return cv.TM_CCOEFF_NORMED
    
    return None

def find_closest(x, list):
    min = None
    index = None
    for i in range(0, len(list)):
        distance = math.sqrt(((x[1] - x[0]) ** 2) + ((list[i][1] - list[i][0]) ** 2))
        # print(distance)
        if min == None or distance < min:
            min = distance
            index = i

    return list[i]

def fix_hp(hp):
    fixed_hp = 0
    # Fix imperfections of image_to_string to fit the expected values.
    if hp[:2] == '10':
        if hp[:3] == '100':
            fixed_hp = hp[:3]
        else:
            fixed_hp = hp[:2]
    else:
        fixed_hp = hp[:2]

    return to_int(fixed_hp)