import cv2 as cv
from time import sleep

import bimage
import bmath
import settings

def in_character_selection(client):
# Check if in character selection.
    loc = bimage.search_object(dir='icons\\', 
            name='character_selection', 
            method=cv.TM_SQDIFF_NORMED, 
            hl=0, 
            threshold=0.1,
            top_left=client.navigation['top_left'],
            size=client.navigation['window_size'])

    if loc:
        return True

    return False

def inventory_is_open(client):
    loc = bimage.search_object(dir='icons', 
                    name='alchemy', 
                    method=cv.TM_SQDIFF, 
                    hl=0, 
                    threshold=20,
                    top_left=client.navigation['top_left'],
                    size=client.navigation['window_size'])

    if loc:
        return True
    
    return False

def is_stuck(client, relative_values):
    hp = get_hp(client, relative_values)
    stuck = False
    if len(client.hp_history) > 0:
        stuck = hp > client.hp_history[-1]

    if hp == 100 or stuck:
        while len(client.hp_history) <= 5:
            client.hp_history.append(get_hp(client, relative_values))
            sleep(1)
    
    if len(client.hp_history) < 5:
        client.hp_history.append(hp)
        print('HP History:', client.hp_history)
    elif len(client.hp_history) >= 5:
        print('HP History:', client.hp_history)
        same_hp = 0
        for i in range(1, len(client.hp_history)):
            if client.hp_history[i] >= client.hp_history[i - 1]:
                same_hp += 1

        if same_hp > 3:
            print('Stuck.')
            return client, True

    return client, False

def kicked(client):
    loc = bimage.search_object(dir='icons', 
                name='login', 
                method=cv.TM_SQDIFF, 
                hl=0, 
                threshold=20,
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])

    if loc:
        return True

    return False

def dead(client):
    loc = bimage.search_object(dir='icons', 
            name='revive', 
            method=cv.TM_SQDIFF_NORMED, 
            hl=0, 
            threshold=0.2,
            top_left=client.navigation['top_left'],
            size=client.navigation['window_size'])

    if loc:
        return True

    return False

def get_hp(client, relative_values):
    top_left = settings.get_value_by_name(relative_values, 'top-left').value
    hp = settings.get_value_by_name(relative_values, 'hp').value
    pos = bmath.get_relative(top_left, client.navigation['top_left'], hp)
    size = settings.get_value_by_name(relative_values, 'hp-rectangle').value

    text = bimage.get_text(point=pos, size=size, pars='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789%')

    # Fix imperfections to fit the expected values.
    text = bmath.fix_hp(text)

    return text

def is_farming(client):
    loc = bimage.search_object(dir='icons\\',
        name='questionmark',
        method=cv.TM_SQDIFF_NORMED, 
        hl=0, 
        threshold=0.2,
        top_left=client.navigation['top_left'],
        size=client.navigation['window_size'])

    if loc:
        return True

    return False