import binput
import keyboard
from time import sleep

task_bar = (182, 1064)
loop = 1
binput.left_click(task_bar)
keyboard.press('space')
sleep(0.1)
while True:
    print('Loop:', loop, 'Activating cape.')
    binput.press_button('2')
    sleep(10)
    loop += 1