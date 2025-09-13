from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from app.main import Bot
import itertools
import cv2 as cv
from loguru import logger

DEBUG_MODE = True

WINDOW_NAME             = 'Mt2009'
WINDOW_BORDERS_OFFSET   = 8         # pixels
WINDOW_TITLEBAR_OFFSET  = 30        # pixels

HSV_PARAMETERS = {
    "arrow_blue"    : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12},
    "arrow_purple"  : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12},
    "arrow_yellow"  : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12},
    "fishing_rod"   : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12},
    "icon"          : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12},
}

TEMPLATES = {
    "arrow_blue"    : "img/arrow_blue.jpg",
    "arrow_purple"  : "img/arrow_purple.jpg",
    "arrow_yellow"  : "img/arrow_yellow.jpg",
    "fishing_rod"   : "img/fishing_rod.jpg",
    "icon"          : "img/icon.jpg",
}
THRESHOLDS = {
    "arrow_blue"    : 0.5,
    "arrow_purple"  : 0.5,
    "arrow_yellow"  : 0.5,
    "fishing_rod"   : 0.5,
    "icon"          : 0.5,
}

templates_to_use = "icon"
hsv_parameters_to_use = HSV_PARAMETERS["icon"]
thresholds_to_use = THRESHOLDS["icon"]

if __name__ == "__main__":
    window_capturer = WindowCapturer(WINDOW_NAME, WINDOW_BORDERS_OFFSET, WINDOW_TITLEBAR_OFFSET)
    hsv_filter = HsvFilter(hsv_parameters_to_use, gui=True)
    finder = Finder(TEMPLATES)
    bot = Bot(window_capturer, finder, hsv_filter, DEBUG_MODE)


    while True:
        hsv_parameters_from_controls = bot.hsv_filter.get_hsv_filter_from_controls()
        results = bot.find(templates_to_use, thresholds_to_use, hsv_parameters_from_controls)
        logger.debug(f'Results: {results}')

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    print('Latest HSV Filter Configuration:\n',
        f"hMin: {hsv_filter.hsv_parameters['hMin']}\n",
        f"sMin: {hsv_filter.hsv_parameters['sMin']}\n",
        f"vMin: {hsv_filter.hsv_parameters['vMin']}\n",
        f"hMax: {hsv_filter.hsv_parameters['hMax']}\n",
        f"sMax: {hsv_filter.hsv_parameters['sMax']}\n",
        f"vMax: {hsv_filter.hsv_parameters['vMax']}\n",
        f"sAdd: {hsv_filter.hsv_parameters['sAdd']}\n",
        f"sSub: {hsv_filter.hsv_parameters['sSub']}\n",
        f"vAdd: {hsv_filter.hsv_parameters['vAdd']}\n",
        f"vSub: {hsv_filter.hsv_parameters['vSub']}\n",
        )
