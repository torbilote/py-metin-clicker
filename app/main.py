import cv2 as cv
import numpy as np
import os
from time import time
from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from numpy.typing import NDArray
from cv2.typing import MatLike
import itertools

# WINDOW_NAME = 'Mt2009'
DEBUG = True

if DEBUG:
    WindowCapturer.list_window_names()

# window = WindowCapture(window_name=WINDOW_NAME)

HSV_PARAMETERS = {
    "hMin": 0, 
    "sMin": 0, 
    "vMin": 63, 
    "hMax": 179, 
    "sMax": 200, 
    "vMax": 255, 
    "sAdd": 0, 
    "sSub": 0, 
    "vAdd": 0, 
    "vSub": 12, 
}


hsv_filter = HsvFilter(gui=True, **HSV_PARAMETERS)
finder = Finder(templates_paths=[
    "img/arrow_purple.jpg",
    "img/fishing_rod.jpg",
        ]
    )

while True:
    # screenshot = window.get_screenshot()
    screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

    processed_screenshot = hsv_filter.apply_hsv_filter(screenshot)
    # processed_screenshot = screenshot

    finding_results = finder.find_images(processed_screenshot, threshold=0.9)

    if DEBUG:
        print([finding_results])
        templates_rectangles = itertools.chain(*finding_results.values())
        Drawer.draw_rectangles(processed_screenshot, templates_rectangles)
        
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

if DEBUG:
    print('Latest HSV Filter Configuration:\n',
        f"hMin: {hsv_filter.hMin}\n",
        f"sMin: {hsv_filter.sMin}\n",
        f"vMin: {hsv_filter.vMin}\n",
        f"hMax: {hsv_filter.hMax}\n",
        f"sMax: {hsv_filter.sMax}\n",
        f"vMax: {hsv_filter.vMax}\n",
        f"sAdd: {hsv_filter.sAdd}\n",
        f"sSub: {hsv_filter.sSub}\n",
        f"vAdd: {hsv_filter.vAdd}\n",
        f"vSub: {hsv_filter.vSub}\n",
        )