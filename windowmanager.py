import win32gui
import pywinauto
import pyautogui
from PIL import ImageGrab, Image
import numpy as np
from time import sleep
import keyboard

def take_screenshot():
    image = pyautogui.screenshot()
    # image = ImageGrab.grab(bbox).convert("RGB")
    image = np.array(image)
    image = image[:, :, ::-1].copy()

    # cv.imshow('Result', image)
    # cv.waitKey()
    
    return image

def leftClick(loc):
    pyautogui.moveTo(loc, duration=0.3, tween=pyautogui.easeInOutQuad)
    pyautogui.click(loc)

def rightClick(loc):
    pyautogui.moveTo(loc, duration=0.3, tween=pyautogui.easeInOutQuad)
    pyautogui.rightClick(loc[0], loc[1])

def press_button(button, time):
    keyboard.press(button)
    sleep(time)
    keyboard.release(button)