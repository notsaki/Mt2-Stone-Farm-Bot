import win32gui
import pywinauto
import pyautogui
from PIL import ImageGrab, Image
import numpy as np
from time import sleep
import keyboard

# sys.path.insert(1, 'autohot')

# from interception import  *
# from consts import *

def take_screenshot():
    image = pyautogui.screenshot()
    # image = ImageGrab.grab(bbox).convert("RGB")
    image = np.array(image)
    image = image[:, :, ::-1].copy()

    # cv.imshow('Result', image)
    # cv.waitKey()
    
    return image

# def moveHandler():
#     if not(event.flags & InterceptionMouseFlag.INTERCEPTION_MOUSE_MOVE_ABSOLUTE):
#         event.x = cords[0]
#         event.y = cords[1]
#     autohotpy.sendToDefaultMouse(event)

def left_click(loc=(0, 0), dur=0.5):
    pyautogui.moveTo(loc, duration=dur, tween=pyautogui.easeInOutQuad)
    pyautogui.click(loc)
    # stroke = InterceptionMouseStroke()
    # stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
    # autohotpy.sendToDefaultMouse(stroke)
    # stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
    # autohotpy.sendToDefaultMouse(stroke)

def right_click(loc=(0, 0), dur=0.3):
    pyautogui.moveTo(loc, duration=dur, tween=pyautogui.easeInOutQuad)
    pyautogui.click(button='right')
    # stroke = InterceptionMouseStroke() # I highly suggest you to open InterceptionWrapper to read which attributes this class has
    
    # #To simulate a mouse click we manually have to press down, and release the buttons we want.
    # stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
    # autohotpy.sendToDefaultMouse(stroke)
    # stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
    # autohotpy.sendToDefaultMouse(stroke)

def double_press(key1, key2):
    keyboard.press(key1)
    sleep(0.1)
    keyboard.press(key2)
    sleep(0.1)
    keyboard.release(key1)
    sleep(0.1)
    keyboard.release(key2)
    sleep(0.1)

def press_button(button=None, time=0.1):
    keyboard.press(button)
    sleep(time)
    keyboard.release(button)
    sleep(0.1)

def inside_the_window(loc=(0, 0), top_left=(0, 0), size=(0, 0)):
    bottom_right = (top_left[0] + size[0], top_left[1] + size[1])

    if loc[0] < top_left[0] or loc[1] < top_left[1] or loc[0] > bottom_right[0] or loc[1] > bottom_right[1]:
        return False
    
    return True

# cords = (0, 0)

# def left_click(c=(0, 0)):
#     global cords
#     cords = c
#     auto.registerForMouseMovement(moveHandler)