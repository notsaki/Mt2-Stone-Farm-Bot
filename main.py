from PIL import ImageGrab, Image
from time import sleep
import cv2 as cv

import binput
import bimage
import bfile
import classes
import bmath
import settings
import actions
import status

def get_status():
    # Dead.
    if status.dead():
        return 'Dead'

    # Kicked.
    if status.kicked():
        return 'Kicked'
    
    # Character selection.
    if status.in_character_selection():
        return 'Character Selection'

    # Check if player is Farming.
    if status.is_farming():
        if status.is_stuck():
            return 'Stuck'
        return 'Farming'
    
    return 'Not Farming'

settings.init()

loop = 1

last_id = 0

while True:
    i = 0
    while i < len(settings.clients):
        settings.client = settings.clients[i]
        print('\nLoop:', loop)
        print('Player:', settings.client.name)

        binput.press_button('z')

        if not settings.client.id == last_id:
            binput.left_click(settings.client.navigation['task_bar'])

        if not settings.client.status == 'Lost':
            settings.client.status = get_status()

        print('Status:', settings.client.status)

        if settings.client.count_stuck >= 5:
            settings.client.count_stuck = 0
            actions.reset()

        elif settings.client.status == 'Kicked':
            actions.login()
            if actions.character_selection():
                actions.setup()
                settings.client.hp_history = []
                actions.close_hud()
            else:
                print('Abort.')

        elif settings.client.status == 'Character Selection':
            if actions.character_selection():
                actions.setup()
                settings.client.hp_history = []
            else:
                print('Abort.')

        elif settings.client.status == 'Stuck':
            actions.unstuck()
            settings.client.hp_history = []
            settings.client.status = 'Not Farming'

        elif settings.client.status == 'Lost':
            binput.press_button('z')
            actions.reset()
            actions.close_hud()
            settings.client.status = 'Not Farming'
            settings.client.hp_history = []

        elif settings.client.status == 'Not Farming':
            settings.client.hp_history = []
            binput.press_button('z')
            if actions.start_farming():    
                settings.client.status = 'Farming'
            else:
                settings.client.status = 'Lost'

        elif settings.client.status == 'Farming':
            hp = status.get_hp()
            print('Stone HP:', hp)
            settings.client.count_stuck = settings.client.count_stuck
            if settings.client.count_stuck >= 5:
                settings.client.hp_history = []
                binput.press_button('z')
                actions.reset()

        elif settings.client.status == 'Dead':
            actions.revive()
            settings.client.status = 'Not Farming'

        else:
            print('Something\'s wrong.')

        binput.press_button('z')

        last_id = settings.client.id

        loop += 1
        if len(settings.client.hp_history) >= 5:
            settings.client.hp_history = []

        settings.clients[i] = settings.client
        if settings.client.status == 'Farming':
            i += 1