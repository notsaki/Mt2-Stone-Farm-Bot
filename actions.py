import cv2 as cv
from time import sleep

import binput
import settings
import bmath
import bimage
import status

def loading_screen(client):
    sleep(1)
    # Loading screen.
    print('Loading screen...')
    count = 0
    # Wait until the inventory image appears. This will mean player is connected.
    loc = bimage.search_object(dir='icons', 
                name='inventory', 
                method=cv.TM_SQDIFF_NORMED, 
                hl=0, 
                threshold=0.2,
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])
    
    for i in range(0, 500):
        loc = bimage.search_object(dir='icons', 
                name='inventory', 
                method=cv.TM_SQDIFF_NORMED, 
                hl=0, 
                threshold=0.38,
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])
                
        if loc:
            count += 1
            if count >= 10:
                break
        

    if count >= 3:
        return True

    return False

def character_selection(client):
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

    return loading_screen(client)

def login(client, relative_values):
    i = 0
    max = 20
    point = settings.get_value_by_name(relative_values, 'channel' + str(client.channel)).value
    top_left = settings.get_value_by_name(relative_values, 'top-left').value

    pos = bmath.get_relative(top_left, client.navigation['top_left'], point)

    binput.left_click(pos)

    while i < max and status.kicked(client):
        point = settings.get_value_by_name(relative_values, 'account' + str(client.id)).value
        top_left = settings.get_value_by_name(relative_values, 'top-left').value

        pos = bmath.get_relative(top_left, client.navigation['top_left'], point)
        
        binput.left_click(pos)

        i += 1
    
    
    if i == max:
        binput.press_button('enter')
        return False
    
    return True

def revive(client, maps, relative_values):
    top_left = settings.get_value_by_name(relative_values, 'top-left').value
    revive = settings.get_value_by_name(relative_values, 'revive-here').value
    top_left = bmath.get_relative(top_left, client.navigation['top_left'], revive)
    size = settings.get_value_by_name(relative_values, 'revive-rectangle').value

    pos = bmath.find_centre(top_left, size)
    while status.dead(client) and not status.kicked(client):
        binput.left_click(pos)

    unstuck(client, maps, relative_values)

def unstuck(client, maps, relative_values):
    x = settings.get_value_by_name(relative_values, 'stone-bar-close').value
    top_left = settings.get_value_by_name(relative_values, 'top-left').value
    pos = bmath.get_relative(top_left, client.navigation['top_left'], x)
    binput.left_click(pos)

    binput.press_button('z')
    binput.press_button(client.horse_slash, 0.1)
    binput.press_button('w', 3)
    sleep(1)
    pos = bmath.find_centre(client.navigation['top_left'], client.navigation['window_size'])
    pos = (pos[0], pos[1] + 70)              
    binput.left_click(pos)

def go_to_map(client, maps, relative_values):
    map = settings.get_value_by_name(maps, client.map)
    if map:
        binput.press_button(client.ring)
        for n in map.navigation:
            top_left = settings.get_value_by_name(relative_values, 'top-left').value
            pos = bmath.get_relative(top_left, client.navigation['top_left'], n)
            binput.left_click(pos, 0.2)

        if loading_screen(client):
            sleep(3)
            print('Teleported.')
            top_left = settings.get_value_by_name(relative_values, 'top-left').value
            mini_map = settings.get_value_by_name(relative_values, 'mini-map').value
            pos = bmath.get_relative(top_left, client.navigation['top_left'], mini_map)
            binput.left_click(pos)

            return True

    return False

def reset_skills(client):
    if client.skills:
        print('Reseting skills...')
        binput.double_press('Ctrl', 'g')

        for i in client.skills:
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
    # binput.press_button('e', 1)

def reset(client, maps, relative_values):
    if go_to_map(client, maps, relative_values):
        calibrate_screen()
        reset_skills(client)

        return True
    
    print('Abort.')
    return False

def setup(client, maps, relative_values):
    sleep(3)
    print('Connected.')
    calibrate_screen()
    reset_skills(client)
    binput.press_button('z')
    start_farming(client, maps, relative_values)

def start_farming(client, maps, relative_values):
    if status.inventory_is_open(client):
        binput.press_button('i')

    sleep(0.1)
    binput.press_button('z', 0.5)
    loc = start_search(client, maps)
    if loc:
        select_target(loc)

        return True

    print('Can\'t find stone.')
    return False


def search(client, maps):
    print('Searching for stone...')
    map = settings.get_value_by_name(maps, client.map)
    loc = bimage.search_all(dir=map.dir, 
                method=cv.TM_SQDIFF_NORMED,
                hl=map.object_detection['hl'],
                threshold=map.object_detection['threshold'],
                top_left=client.navigation['top_left'],
                size=client.navigation['window_size'])

    # loc = bimage.search_object(dir=maps[client.map].dir, 
    #             method=cv.TM_SQDIFF_NORMED,
    #             hl=maps[client.map].object_detection['hl'],
    #             threshold=maps[client.map].object_detection['threshold'],
    #             top_left=client.navigation['top_left'],
    #             size=client.navigation['window_size'])
    
    if loc:
        top_left = (0, 0)
        for i in range(0, len(loc)):
            loc[i] = bmath.get_relative(top_left, client.navigation['top_left'], loc[i])

        centre = bmath.find_centre(client.navigation['top_left'], client.navigation['window_size'])
        point = bmath.find_closest(centre, loc)
        # print(point)
        
        return (int(point[0]), int(point[1]))

    return None

def start_search(client, maps):
    loc = search(client, maps)

    if loc:
        return loc

    for i in range(0, 7):
        binput.press_button(button='e', time=0.5)

        loc = search(client, maps)

        if loc:
            return loc

    return None