import pyautogui

while True:
    input('Point your cursor to the window on task bar and press enter.')
    pos = pyautogui.position()
    print(str(pos[0]) + ',', pos[1])