import cv2 as cv
from time import sleep

import bimage
import bmath
import settings

def hud(name, threshold=20):
    loc = bimage.search_object(dir='icons\\hud\\', 
                    name=name, 
                    method=cv.TM_SQDIFF, 
                    hl=0, 
                    threshold=threshold,
                    top_left=settings.client.navigation['top_left'],
                    size=settings.client.navigation['window_size'])

    if loc:
        return True
    
    return False

def in_character_selection():
# Check if in character selection.
    loc = bimage.search_object(dir='icons\\', 
            name='character_selection', 
            method=cv.TM_SQDIFF_NORMED, 
            hl=1, 
            threshold=0.5,
            top_left=settings.client.navigation['top_left'],
            size=settings.client.navigation['window_size'])

    if loc:
        return True

    return False    

def is_stuck():
    hp = get_hp()
    stuck = False
    if len(settings.client.hp_history) > 0:
        stuck = hp > settings.client.hp_history[-1]

    if hp == 100 or stuck:
        while len(settings.client.hp_history) <= 5:
            settings.client.hp_history.append(get_hp())
            sleep(1)
    
    if len(settings.client.hp_history) < 5:
        settings.client.hp_history.append(hp)
        print('HP History:', settings.client.hp_history)
    elif len(settings.client.hp_history) >= 5:
        print('HP History:', settings.client.hp_history)
        same_hp = 0
        for i in range(1, len(settings.client.hp_history)):
            if settings.client.hp_history[i] >= settings.client.hp_history[i - 1]:
                same_hp += 1

        if same_hp > 3:
            print('Stuck.')
            settings.client.count_stuck += 1
            return True

    return False

def kicked():
    loc = bimage.search_object(dir='icons', 
                name='login', 
                method=cv.TM_SQDIFF, 
                hl=0, 
                threshold=20,
                top_left=settings.client.navigation['top_left'],
                size=settings.client.navigation['window_size'])

    if loc:
        return True

    return False

def dead():
    loc = bimage.search_object(dir='icons', 
            name='revive', 
            method=cv.TM_SQDIFF_NORMED, 
            hl=0, 
            threshold=0.2,
            top_left=settings.client.navigation['top_left'],
            size=settings.client.navigation['window_size'])

    if loc:
        return True

    return False

def get_hp():
    top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value
    hp = settings.get_value_by_name(settings.relative_values, 'hp').value
    pos = bmath.get_relative(top_left, settings.client.navigation['top_left'], hp)
    size = settings.get_value_by_name(settings.relative_values, 'hp-rectangle').value

    text = bimage.get_text(point=pos, size=size, pars='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789%')

    # Fix imperfections to fit the expected values.
    text = bmath.fix_hp(text)

    return text

def is_farming():
    loc = bimage.search_object(dir='icons\\',
        name='questionmark',
        method=cv.TM_SQDIFF_NORMED, 
        hl=0, 
        threshold=0.2,
        top_left=settings.client.navigation['top_left'],
        size=settings.client.navigation['window_size'])

    if loc:
        return True

    return False