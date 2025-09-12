import pydirectinput
import pyautogui
import time

x = 'siema elo'

for i in x:
    pydirectinput.press(i)
    pyautogui.press(i)
    time.sleep(0.2)
    print(i)
