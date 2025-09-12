from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
import cv2 as cv
import itertools
from enum import Enum
import time
from loguru import logger
import pydirectinput
from cv2.typing import Rect
from typing import Sequence


DEBUG_MODE = True

WINDOW_NAME = 'Mt2009'
WINDOW_BORDERS_OFFSET = 8 # pixels
WINDOW_TITLEBAR_OFFSET = 30 # pixels

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

TIME_BEGINNING              = 5 # seconds
TIME_AFTER_ICON_APPEARS     = 5 # seconds
TIME_PAUSE_BEFORE_FISHING   = 5 # seconds
TIME_FISHING                = 0.4 # seconds
TIME_FISHING_ARROW_BLUE     = TIME_FISHING * 2 # seconds
TIME_FISHING_ARROW_PURPLE   = TIME_FISHING / 2 # seconds
TIME_FISHING_ARROW_YELLOW   = TIME_FISHING / 4 # seconds

KEY_WORM    = '2'
KEY_FISHING = 'space'

class Step(Enum):
    STEP_1: int = 1 # wait
    STEP_2: int = 2 # press '2'
    STEP_3: int = 3 # press 'space'
    STEP_4: int = 4 # find 'icon'
    STEP_5: int = 5 # wait 
    STEP_6: int = 6 # press 'space'
    STEP_7: int = 7 # wait
    STEP_8: int = 8 # find 'fishing_rod'
    STEP_9: int = 9 # press 'space' and find 'arrow'
    STEP_10: int = 10 # press 'space' and find 'arrow'
    STEP_11: int = 11 # press 'space' and find 'fishing_rod'

class Bot:
    def __init__(self, window_capturer: WindowCapturer, finder: Finder, hsv_filter: HsvFilter, debug_mode: bool) -> None:
        self.debug_mode = debug_mode
        
        self.window_capturer = window_capturer
        self.finder = finder
        self.hsv_filter = hsv_filter

    def _wait(self, seconds: int) -> None:
        for i in range(seconds):
            logger.debug(f'Waiting for {seconds - i} more seconds..')
            time.sleep(i)

    def _press(self, key_name: str) -> None:
        logger.debug(f'Pressing key: {key_name}..')
        time.sleep(0.05)
        pydirectinput.press(key_name)
        time.sleep(0.05)
        logger.debug(f'Key pressed.')

    def _find(self, template: str | list[str], threshold: int | list[int]) -> dict[str,Sequence[Rect]]:
        screenshot_raw = self.window_capturer.get_screenshot()
        results = dict()

        if isinstance(template, list) and isinstance(threshold, list):
            for template, threshold in zip(template, threshold):
                self.hsv_filter.hsv_parameters = HSV_PARAMETERS[template]
                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)
                results[template] = self.finder.find_template(template, screenshot_hsv, threshold)
        else:
            self.hsv_filter.hsv_parameters = HSV_PARAMETERS[template]
            screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)
            results[template] = self.finder.find_template(template, screenshot_hsv, threshold)
            
        if self.debug_mode:
            logger.debug(f'Finding results of {template}:\n {results}')
            templates_rectangles = itertools.chain(*results.values())
            Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)
        
        return results


    def run(self) -> None:
        step = Step.STEP_1

        while True:
            if self.debug_mode:
                WindowCapturer.list_window_names()
            
            if step == Step.STEP_1:
                self._wait(TIME_BEGINNING)
                step = Step.STEP_2

            if step == Step.STEP_2:
                self._press(KEY_WORM)
                step = Step.STEP_3

            if step == Step.STEP_3:
                self._press(KEY_FISHING)
                step = Step.STEP_4

            if step == Step.STEP_4:
                findings = self._find('icon', THRESHOLDS["icon"])
                if findings['icon']:
                    step = Step.STEP_5

            if step == Step.STEP_5:
                self._wait(TIME_AFTER_ICON_APPEARS)
                step = Step.STEP_6

            if step == Step.STEP_6:
                self._press(KEY_FISHING)
                step = Step.STEP_7

            if step == Step.STEP_7:
                self._wait(TIME_PAUSE_BEFORE_FISHING)
                step = Step.STEP_8

            if step == Step.STEP_8:
                findings = self._find('fishing_rod', THRESHOLDS["fishing_rod"])
                if findings['fishing_rod']:
                    step = Step.STEP_9
                else:
                    step = Step.STEP_1
            
            if step == Step.STEP_9:
                self._press(KEY_FISHING)
                findings = self._find(['arrow_blue', 'arrow_purple', 'arrow_yellow'], [THRESHOLDS["arrow_blue"], THRESHOLDS["arrow_purple"], THRESHOLDS["arrow_yellow"]])
                if any(findings['arrow_blue'], findings['arrow_purple'], findings['arrow_yellow']):
                    step = Step.STEP_10
                else:
                    self._wait(0.4)

            if step == Step.STEP_10:
                self._press(KEY_FISHING)
                findings = self._find(['arrow_blue', 'arrow_purple', 'arrow_yellow'], [THRESHOLDS["arrow_blue"], THRESHOLDS["arrow_purple"], THRESHOLDS["arrow_yellow"]])
                if findings['arrow_blue']:
                    self._wait(0.8)
                elif findings['arrow_purple']:
                    self._wait(0.2)
                elif findings['arrow_yellow']:
                    self._wait(0.1)
                else:
                    step = Step.STEP_11

            if step == Step.STEP_11:
                self._press(KEY_FISHING)
                findings = self._find('fishing_rod', THRESHOLDS["fishing_rod"])
                if findings['fishing_rod']:
                    self._wait(0.4)
                else:
                    step = Step.STEP_1          
    
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

if __name__ == "__main__":
    window_capturer = WindowCapturer(WINDOW_NAME, WINDOW_BORDERS_OFFSET, WINDOW_TITLEBAR_OFFSET)
    hsv_filter = HsvFilter()
    finder = Finder(TEMPLATES)
    bot = Bot(window_capturer, finder, hsv_filter, DEBUG_MODE)

    bot.run()