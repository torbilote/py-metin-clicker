import cv2 as cv
import numpy as np
import os
from time import time
from app.windowcapture import WindowCapture
from app.hsvfilter import HsvFilter
from numpy.typing import NDArray
from cv2.typing import MatLike


WINDOW_NAME = 'Mt2009'
DEBUG = True

if DEBUG:
    WindowCapture.list_window_names()

window = WindowCapture(window_name=WINDOW_NAME)
hsv_filter = HsvFilter(gui=True)


while True:
    screenshot = window.get_screenshot()

    processed_image = hsv_filter.apply_hsv_filter(screenshot)

    cv.imshow('Image', processed_image)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break