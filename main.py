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

import binput
import bimage
import bfile
import classes
import bmath

client = None

def init_settings():
    clnt, maps, relatives, s = bfile.get_settings()
    cl = []
    ma = {}

    # Normalize data.
    for i in clnt:
        if i['account']['enabled'] == 'true':
            name = i['account']['username']
            pos = i['position']['pos']
            map = i['account']['map']
            id = i['account'].getint('id')
            navigation = {
                'task_bar': bmath.get_tuple(i['navigation']['task-bar']), 
                'top_left': bmath.get_tuple(i['navigation']['top-left']), 
                'window_size': bmath.get_tuple(i['navigation']['window-size'])
            }
            skills = []
            for k, j in i['skills'].items():
                skills.append(j)

            cl.append(classes.Client(id=int(id), 
                                    name=name, 
                                    map=map, 
                                    skills=skills, 
                                    status='kicked', 
                                    pos=pos, 
                                    navigation=navigation, 
                                    same_hp_count=0, 
                                    prev_hp=101, 
                                    not_found=0))

    for i in range(0, len(maps)):
        name = maps[i]['map']['name']
        dir = maps[i]['stone-sample']['dir']
        navigation = [
            bmath.get_tuple(maps[i]['navigation']['menu']), 
            bmath.get_tuple(maps[i]['navigation']['area'])
        ]
        object_detection = {
            'method': bmath.method_to_const(maps[i]['object-detection']['method']), 
            'hl': maps[i]['object-detection'].getint('hl'), 
            'threshold': maps[i]['object-detection'].getfloat('threshold')
        }

        ma.update({name: classes.Map(dir, navigation, object_detection)})

    return cl, ma, relatives, s

c, m, relatives, settings = init_settings()

def in_character_selection():
    # Check if in character selection.
    loc = bimage.search_object(dir='icons', 
                name='select_player', 
                method=cv.TM_SQDIFF_NORMED, 
                hl=0, 
                threshold=0.2,
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])

    if loc == None:
        return False

    return True

def character_selection():
    # Select player.
    print('Character selection.')
    if client.pos == 'left':
        binput.press_button(button='left')
    elif client.pos == 'right':
        binput.press_button(button='right')
    elif client.pos == 'back':
        binput.press_button(button='right')
        binput.press_button(button='right')

    binput.press_button(button='enter')

    loading_screen()


def loading_screen():
    # Loading screen.
    print('Loading screen...')

    # Wait until the inventory image appears. This will mean player is connected.
    loc = bimage.search_object(dir='icons', 
                name='inventory', 
                method=cv.TM_SQDIFF_NORMED, 
                hl=0, 
                threshold=0.2,
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])
    
    for i in range(0, 50):
        loc = bimage.search_object(dir='icons', 
                name='inventory', 
                method=cv.TM_SQDIFF_NORMED, 
                hl=0, 
                threshold=0.2,
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])

        if loc:
            return

def login():
    i = 0
    max = 20
    while i < max and kicked():
        pos = {'x': None, 'y': None}

        for k, r in relatives.items():
            if 'account' in k:
                if client.id == r.getint('id'):
                    pos['x'] = r['x']
                    pos['y'] = r['y']
                    break

        pos = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], pos)

        size = (relatives['account-rectangle'].getint('w'), relatives['account-rectangle'].getint('h'))
        pos = bmath.find_centre(pos, size)
        
        binput.left_click(pos)

        i += 1
    
    
    if i == max:
        binput.press_button('enter')
        return False
    
    return True

def is_farming():
    prev_hp = 101
    count = 0
    loops = 10
    # hp100 = 0
    # hp0 = 0
    for i in range(0, loops):
        loc = bimage.search_object(dir='icons\\hp',
            method=cv.TM_SQDIFF_NORMED, 
            hl=0, 
            threshold=0.4,
            top_left=client.navigation['top_left'],
            size=client.navigation['window_size'])
        
        if not loc:
            count += 1
            # hp = get_hp()
            
            # if hp == 100:
            #     hp100 += 1

            # if hp >= prev_hp:
            #     count += 1

        # prev_hp = hp

        # sleep(1)

    # print('Count:', count)

    # if hp100 >= loops:
    #     return False
    # print(count)
    if count > 8:
        return False
    
    return True

def start_search():
    loc = search()

    if loc:
        return loc

    for i in range(0, 7):
        binput.press_button(button='e', time=0.5)

        loc = search()

        if loc:
            return loc

    return None

def get_status():
    # Dead.
    if dead():
        return 'dead'

    # # Kicked.
    # if kicked():
    #     return 'kicked'
    
    # Character selection.
    if in_character_selection():
        return 'character_selection'

    # Check if player is farming.
    if is_farming():
        return 'farming'
    
    return 'not_farming'
        

def kicked():
    # point = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['account1'])

    # size = (relatives['account-rectangle'].getint('w'), relatives['account-rectangle'].getint('h'))

    # text = bimage.get_text(point=point, size=size, pars='--psm 8 --oem 1')

    # if c[0].name[:2] in text:
    #     return True
    
    # return False

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


def revive():
    top_left = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['revive-city-button'])
    size = (relatives['revive-rectangle'].getint('w'), relatives['revive-rectangle'].getint('h'))

    pos = bmath.find_centre(top_left, size)
    while dead() and not kicked() and not in_character_selection():
        binput.left_click(pos)

    loading_screen()

def dead():
    pos = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['revive-city-button'])
    size = (relatives['revive-rectangle'].getint('w'), relatives['revive-rectangle'].getint('h'))

    text = bimage.get_text(point=pos, size=size, pars='--psm 8 --oem 1')

    if 'Res' in text:
        return True

    return False

def get_hp():
    pos = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['hp'])
    size = (relatives['hp-rectangle']['w'], relatives['hp-rectangle']['h'])

    text = bimage.get_text(point=pos, size=size, pars='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789%')

    # Fix imperfections to fit the expected values.
    text = fix_hp(text)

    return bmath.to_int(text)

def fix_hp(hp):
    # Fix imperfections of image_to_string to fit the expected values.
    if hp[:2] == '10':
        if hp[:3] == '100':
            return hp[:3]
        else:
            return hp[:2]
    else:
        return hp[:2]

def inventory_is_open():
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

def go_to_map():
    # Check if inventory is open.
    # if not inventory_is_open():
    #     binput.press_button(button='i')

    # Inventory first tab.
    # pos = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['first-tab'])
    # binput.left_click(pos)

    # Press the ring.
    # loc = bimage.search_object(dir='icons', 
    #                 name='teleport_ring', 
    #                 method=cv.TM_SQDIFF, 
    #                 hl=1, 
    #                 threshold=20,
    #                 top_left=client.navigation['top_left'],
    #                 size=client.navigation['window_size'])

    # if not loc:
    #     return False
    binput.press_button('3')
    
    pos = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['menu'])
    binput.left_click(pos)

    pos = bmath.get_relative(relatives['top-left'], client.navigation['top_left'], relatives['area'])
    binput.left_click(pos)

    # loc = bmath.window_to_full(loc, client.navigation['top_left'])
    # binput.right_click(loc)

    binput.press_button(button=relatives['ring']['button'], time=0.1)
    
    # # Menu.
    # # index = 0
    # # for i in range(0, len(m)):
    # #     if m[i].name == map_name:
    # #         index = i
    # #         break
    
    # for i in m[client.map].navigation:
    #     pos = bmath.get_relative2(relatives['top-left'], client.navigation['top_left'], i)

    #     binput.left_click(pos)

    loading_screen()

    print('Teleported.')

    return True


def search():
    print('Searching for stone...')
    loc = bimage.search_all(dir=m[client.map].dir, 
                method=cv.TM_SQDIFF_NORMED,
                hl=m[client.map].object_detection['hl'],
                threshold=m[client.map].object_detection['threshold'],
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])

    # loc = bimage.search_object(dir=m[client.map].dir, 
    #             method=cv.TM_SQDIFF_NORMED,
    #             hl=m[client.map].object_detection['hl'],
    #             threshold=m[client.map].object_detection['threshold'],
    #             top_left=client.navigation['top_left'],
    #             size=client.navigation['window_size'])
    
    if loc:
        top_left = (0, 0)
        for i in range(0, len(loc)):
            loc[i] = bmath.get_relative3(top_left, client.navigation['top_left'], loc[i])

        centre = bmath.find_centre(client.navigation['top_left'], client.navigation['window_size'])
        point = bmath.find_closest(centre, loc)
        # print(point)
        
        return (int(point[0]), int(point[1]))

    return None

def reset_skills():
    print('Reseting skills...')
    binput.double_press('Ctrl', 'g')

    # binput.press_button(button='F2', time=3)
    # binput.press_button(button='4', time=1)

    for i in client.skills:
        binput.press_button(button=i, time=2)

    binput.double_press('Ctrl', 'g')

    print('Done')

def calibrate_screen():
    print('Calibrating...')

    binput.press_button(button='r', time=2)
    binput.press_button(button='f', time=0.8)
    binput.press_button(button='g', time=4)
    binput.press_button(button='t', time=0.7)

    print('Calibration done.')

loop = 1
reset = True

last_id = 0

while True:
    for cl in c:
        client = cl
        print('\nLoop:', loop)
        print('Player:', cl.name)

        # binput.press_button('z')

        if not cl.id == last_id:
            binput.left_click(cl.navigation['task_bar'])

        if not cl.status == 'lost' and not cl.status == 'stuck':
            cl.status = get_status()

        print('Status:', cl.status)

        if cl.status == 'stuck':
            # binput.press_button('esc')
            cl.status = 'not_farming'

        if cl.status == 'kicked':
            login()
        elif cl.status == 'character_selection':
            character_selection()
            print('Connected.')
        elif cl.status == 'lost':
            if go_to_map():
                calibrate_screen()
                reset_skills()

            cl.status = 'not_farming'
        elif cl.status == 'not_farming':
            sleep(0.1)
            binput.press_button('z', 0.5)
            # Double check.
            cl.status = get_status()
            print('Status:', get_status())
            if cl.status == 'not_farming':
                pos = bmath.find_centre(cl.navigation['top_left'], cl.navigation['window_size'])
                if inventory_is_open():
                    binput.press_button(button='i')

                loc = start_search()
                if loc:
                    print('Found stone at', loc)
                    loc = (loc[0], loc[1] + 120)
                    binput.left_click(loc)
                    binput.press_button('e', 1.5)
                else:
                    print('Can\'t find stone.')
                    cl.status = 'lost'
                    pos = bmath.find_centre(cl.navigation['top_left'], cl.navigation['window_size'])
                    binput.left_click(pos)
        elif cl.status == 'farming':
            hp = get_hp()
            if hp == 100:
                while len(cl.hp_history) <= 5:
                    cl.hp_history.append(get_hp())

            if len(cl.hp_history) < 5:
                cl.hp_history.append(hp)
                print('HP History:', cl.hp_history)
            elif len(cl.hp_history) >= 5:
                same_hp = 0
                for i in range(1, len(cl.hp_history)):
                    if cl.hp_history[i] >= cl.hp_history[i - 1]:
                        same_hp += 1

                if same_hp > 3:
                    print('Stuck.')
                    binput.press_button('space', 5)
                    cl.status = 'stuck'

                cl.hp_history = []
            print('Stone HP:', hp)
        elif cl.status == 'dead':
            revive()
            if go_to_map():
                calibrate_screen()
        else:
            print('Something\'s wrong.')

        last_id = cl.id

        loop += 1