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

client = None

def get_status():
    global client

    # Dead.
    if status.dead(client):
        return 'Dead'

    # Kicked.
    if status.kicked(client):
        return 'Kicked'
    
    # Character selection.
    if status.in_character_selection(client):
        return 'Character Selection'

    # Check if player is Farming.
    if status.is_farming(client):
        client, stuck = status.is_stuck(client, relative_values)
        if stuck:
            client.count_stuck += 1
            return 'Stuck'
        return 'Farming'
    
    return 'Not Farming'

clients, maps, relative_values = settings.init_settings()

loop = 1

last_id = 0

while True:
    i = 0
    while i < len(clients):
        client = clients[i]
        print('\nLoop:', loop)
        print('Player:', client.name)

        binput.press_button('z')

        if not client.id == last_id:
            binput.left_click(client.navigation['task_bar'])

        if not client.status == 'Lost':
            client.status = get_status()

        print('Status:', client.status)

        if client.status == 'Kicked':
            actions.login(client, relative_values)
            if actions.character_selection(client):
                actions.setup(client, maps, relative_values)
                client.hp_history = []
            else:
                print('Abort.')

        elif client.status == 'Character Selection':
            if actions.character_selection(client):
                actions.setup(client, maps, relative_values)
                client.hp_history = []
            else:
                print('Abort.')

        elif client.status == 'Stuck':
            actions.unstuck(client, maps, relative_values)
            client.hp_history = []
            client.status = 'Not Farming'
        elif client.status == 'Lost':
            binput.press_button('z')
            actions.reset(client, maps, relative_values)
            client.status = 'Not Farming'
            client.hp_history = []

        elif client.status == 'Not Farming':
            client.hp_history = []
            binput.press_button('z')
            if actions.start_farming(client, maps, relative_values):    
                client.status = 'Farming'
            else:
                client.status = 'Lost'

        elif client.status == 'Farming':
            hp = status.get_hp(client, relative_values)
            print('Stone HP:', hp)
            client.count_stuck = client.count_stuck
            if client.count_stuck >= 5:
                client.hp_history = []
                binput.press_button('z')
                actions.reset(client, maps, relative_values)

        elif client.status == 'Dead':
            actions.revive(client, maps, relative_values)
            client.status = 'Not Farming'

        else:
            print('Something\'s wrong.')

        binput.press_button('z')

        last_id = client.id

        loop += 1
        if len(client.hp_history) >= 5:
            client.hp_history = []
        clients[i] = client
        if client.status == 'Farming':
            i += 1