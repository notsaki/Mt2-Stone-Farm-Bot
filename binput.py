import pyautogui
import numpy as np
from time import sleep
import keyboard

def take_screenshot():
    image = pyautogui.screenshot()
    image = np.array(image)
    image = image[:, :, ::-1].copy()
    
    return image

def left_click(loc=(0, 0), dur=0.1):
    pyautogui.moveTo(loc, duration=dur, tween=pyautogui.easeInOutQuad)
    pyautogui.click(loc)

def right_click(loc=(0, 0), dur=0.1):
    pyautogui.moveTo(loc, duration=dur, tween=pyautogui.easeInOutQuad)
    pyautogui.click(button='right')

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