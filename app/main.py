import cv2 as cv
import numpy as np
import os
from time import time
from app.windowcapture import WindowCapture
from app.hsvfilter import HsvFilter
from app.finder import Finder
from numpy.typing import NDArray
from cv2.typing import MatLike


# WINDOW_NAME = 'Mt2009'
DEBUG = True

if DEBUG:
    WindowCapture.list_window_names()

# window = WindowCapture(window_name=WINDOW_NAME)
hsv_filter = HsvFilter(gui=True)
finder = Finder(images_paths=[
    "img/toolbar.jpg",
    "img/icon.jpg",
    "img/box.jpg",
    "img/fishing_rod.jpg",
])

while True:
    # screenshot = window.get_screenshot()
    screenshot = cv.imread('img/test.jpg')

    processed_screenshot = hsv_filter.apply_hsv_filter(screenshot)
    
    finder.base_image = processed_screenshot
    results_rectangles = finder.find()
    
    print(results_rectangles)

    cv.imshow('Screenshot', processed_screenshot)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

if DEBUG:
    print('Current HSV Filter Configuration:\n',
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