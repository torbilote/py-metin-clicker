from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
import itertools
import cv2 as cv

WINDOW_NAME = 'Mt2009'
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
TEMPLATES_TO_DETECT = {
    "arrow_blue": "img/arrow_blue.jpg",
    "arrow_purple": "img/arrow_purple.jpg",
    "arrow_yellow": "img/arrow_yellow.jpg",
    "fishing_rod": "img/fishing_rod.jpg",
    "icon": "img/icon2.jpg",
}

if __name__ == "__main__":
    window_capturer = WindowCapturer(WINDOW_NAME)
    hsv_filter = HsvFilter(HSV_PARAMETERS, gui=True)
    finder = Finder(TEMPLATES_TO_DETECT)
    while True:

        # screenshot_raw = window_capturer.get_screenshot()
        screenshot_raw = cv.imread('img/test_icon2.jpg', cv.IMREAD_UNCHANGED)
        screenshot_hsv = hsv_filter.apply_hsv_filter(screenshot_raw)
        finding_results = finder.find_images(['icon'], screenshot_hsv, threshold=0.3)

        print(finding_results)

        templates_rectangles = itertools.chain(*finding_results.values())
        Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)

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
