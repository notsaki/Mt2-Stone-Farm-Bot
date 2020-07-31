import cv2 as cv
from time import sleep

import binput
import settings
import bmath
import bimage
import status

def close_hud():
    print('Checking hud...')
    if status.hud('inventory'):
        binput.press_button('i')

    if status.hud('minimap', 1000000):
        top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value
        mini_map = settings.get_value_by_name(settings.relative_values, 'mini-map').value
        pos = bmath.get_relative(top_left, settings.client.navigation['top_left'], mini_map)
        binput.left_click(pos)
    
    hud_list = ['character', 'friends_list', 'itemshop', 'map', 'menu', 'shop', 'shop2']
    stop = False
    
    while not stop:
        for h in hud_list:
            if status.hud(h):
                binput.press_button('Esc')

        stop = True
        for h in hud_list:
            if status.hud(h):
                stop = False
                break
    print('Done.')

def character_selection():
    # Select player.
    print('Character selection.')
    if settings.client.pos == 'left':
        binput.press_button(button='left')
    elif settings.client.pos == 'right':
        binput.press_button(button='right')
    elif settings.client.pos == 'back':
        binput.press_button(button='right')
        binput.press_button(button='right')

    binput.press_button(button='enter')

    return status.loading_screen()

def login():
    i = 0
    max = 20
    point = settings.get_value_by_name(settings.relative_values, 'channel' + str(settings.client.channel)).value
    top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value

    pos = bmath.get_relative(top_left, settings.client.navigation['top_left'], point)

    binput.left_click(pos)

    while i < max and status.kicked():
        point = settings.get_value_by_name(settings.relative_values, 'account' + str(settings.client.id)).value
        top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value

        pos = bmath.get_relative(top_left, settings.client.navigation['top_left'], point)
        
        binput.left_click(pos)

        i += 1
    
    
    if i == max:
        binput.press_button('enter')
        return False

    return True

def revive():
    top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value
    revive = settings.get_value_by_name(settings.relative_values, 'revive-here').value
    top_left = bmath.get_relative(top_left, settings.client.navigation['top_left'], revive)
    size = settings.get_value_by_name(settings.relative_values, 'revive-rectangle').value

    pos = bmath.find_centre(top_left, size)
    while status.dead() and not status.kicked():
        binput.left_click(pos)

    unstuck()

def unstuck():
    x = settings.get_value_by_name(settings.relative_values, 'stone-bar-close').value
    top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value
    pos = bmath.get_relative(top_left, settings.client.navigation['top_left'], x)
    binput.left_click(pos)

    binput.press_button('z')
    binput.press_button(settings.client.horse_slash, 0.1)
    binput.press_button('w', 3)
    sleep(1)
    pos = bmath.find_centre(settings.client.navigation['top_left'], settings.client.navigation['window_size'])
    pos = (pos[0], pos[1] + 70)              
    binput.left_click(pos)

def go_to_map():
    map = settings.get_value_by_name(settings.maps, settings.client.map)
    if map:
        binput.press_button(settings.client.ring)
        for n in map.navigation:
            top_left = settings.get_value_by_name(settings.relative_values, 'top-left').value
            pos = bmath.get_relative(top_left, settings.client.navigation['top_left'], n)
            binput.left_click(pos, 0.2)

        if status.loading_screen():
            print('Teleported.')
            return True

    return False

def reset_skills():
    if settings.client.skills:
        print('Reseting skills...')
        binput.double_press('Ctrl', 'g')

        for i in settings.client.skills:
            binput.press_button(button=i, time=2)

        binput.double_press('Ctrl', 'g')

        print('Done')

def calibrate_screen():
    print('Calibrating...')

    # binput.press_button(button='r', time=2)
    binput.press_button(button='f', time=1.2)
    binput.press_button(button='g', time=3)
    binput.press_button(button='t', time=0.7)

    print('Calibration done.')

def select_target(loc):
    print('Found stone at', loc)
    loc = (loc[0], loc[1] + 80)
    binput.left_click(loc)
    binput.press_button('e', 0.5)

def reset():
    if go_to_map():
        close_hud()
        calibrate_screen()
        reset_skills()

        return True
    
    print('Abort.')
    return False

def setup():
    print('Connected.')
    close_hud()
    calibrate_screen()
    reset_skills()
    binput.press_button('z')
    start_farming()

def start_farming():
    sleep(0.1)
    binput.press_button('z', 0.5)
    loc = start_search()
    if loc:
        select_target(loc)

        return True

    print('Can\'t find stone.')
    return False


def search():
    print('Searching for stone...')
    map = settings.get_value_by_name(settings.maps, settings.client.map)
    loc = bimage.search_all(dir=map.dir, 
                method=cv.TM_SQDIFF_NORMED,
                hl=map.object_detection['hl'],
                threshold=map.object_detection['threshold'],
                top_left=settings.client.navigation['top_left'],
                size=settings.client.navigation['window_size'])

    # loc = bimage.search_object(dir=settings.maps[settings.client.map].dir, 
    #             method=cv.TM_SQDIFF_NORMED,
    #             hl=settings.maps[settings.client.map].object_detection['hl'],
    #             threshold=settings.maps[settings.client.map].object_detection['threshold'],
    #             top_left=settings.client.navigation['top_left'],
    #             size=settings.client.navigation['window_size'])
    
    if loc:
        top_left = (0, 0)
        for i in range(0, len(loc)):
            loc[i] = bmath.get_relative(top_left, settings.client.navigation['top_left'], loc[i])

        centre = bmath.find_centre(settings.client.navigation['top_left'], settings.client.navigation['window_size'])
        point = bmath.find_closest(centre, loc)
        # print(point)
        
        return (int(point[0]), int(point[1]))

    return None

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