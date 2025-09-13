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
from numpy.typing import NDArray
from cv2.typing import MatLike
from typing import Optional

DEBUG_MODE = True

WINDOW_NAME             = 'Mt2009'
WINDOW_BORDERS_OFFSET   = 8         # pixels
WINDOW_TITLEBAR_OFFSET  = 30        # pixels

HSV_PARAMETERS = {
    "arrow_blue"    : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12}, # TODO to configure
    "arrow_purple"  : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12}, # TODO to configure
    "arrow_yellow"  : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12}, # TODO to configure
    "fishing_rod"   : {"hMin": 0, "sMin": 0, "vMin": 63, "hMax": 179, "sMax": 200, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 12}, # TODO to configure
    "icon"          : {"hMin": 0, "sMin": 0, "vMin": 103, "hMax": 179, "sMax": 49, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 36},
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
    "icon"          : 0.35,
}

TIME_BEGINNING              = 5                 # seconds
TIME_AFTER_ICON_APPEARS     = 5                 # seconds
TIME_PAUSE_BEFORE_FISHING   = 5                 # seconds
TIME_FISHING                = 0.4               # seconds
TIME_FISHING_ARROW_BLUE     = TIME_FISHING * 2  # seconds
TIME_FISHING_ARROW_PURPLE   = TIME_FISHING / 2  # seconds
TIME_FISHING_ARROW_YELLOW   = TIME_FISHING / 4  # seconds

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

    def wait(self, seconds: int) -> None:
        for i in range(seconds):
            logger.debug(f'Waiting for {seconds - i} more seconds..')
            time.sleep(i)

    def press(self, key_name: str) -> None:
        logger.debug(f'Pressing key: {key_name}..')
        time.sleep(0.05)
        pydirectinput.press(key_name)
        time.sleep(0.05)
        logger.debug(f'Key pressed.')

    def apply_filter(self, screenshot_raw: NDArray | MatLike, hsv_parameters: dict[str, int]) ->  NDArray | MatLike:
        self.hsv_filter.hsv_parameters = hsv_parameters
        return self.hsv_filter.apply_hsv_filter(screenshot_raw)

    def find(self, template: str | list[str], threshold: int | list[int], hsv_parameters: dict[str, int] | list[dict[str, int]], mocked_image_path: Optional[str] = None) -> dict[str,Sequence[Rect]]:
        if mocked_image_path:
            screenshot_raw = cv.imread(mocked_image_path, cv.IMREAD_UNCHANGED)
        else:
            screenshot_raw = self.window_capturer.get_screenshot()
        
        results = dict()

        if isinstance(template, list) and isinstance(threshold, list) and isinstance(hsv_parameters, list):
            for template, threshold, hsv_parameters in zip(template, threshold, hsv_parameters):
               screenshot_hsv = self.apply_filter(screenshot_raw, hsv_parameters)
               results[template] = self.finder.find_template(template, screenshot_hsv, threshold)                                                                                                                     
        else:
            screenshot_hsv = self.apply_filter(screenshot_raw, hsv_parameters)
            results[template] = self.finder.find_template(template, screenshot_hsv, threshold)
        
        if self.debug_mode:
            templates_rectangles = itertools.chain(*results.values())
            Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)
        
        return results


    def run(self) -> None:
        if self.debug_mode:
            WindowCapturer.list_window_names()

        step = Step.STEP_1

        while True:
            logger.debug('Started bot.')

            if step == Step.STEP_1:
                logger.debug(f'Started step: {step}.')

                self.wait(TIME_BEGINNING)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_2

            if step == Step.STEP_2:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_WORM)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_3

            if step == Step.STEP_3:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_4

            if step == Step.STEP_4:
                logger.debug(f'Started step: {step}.')

                findings = self.find('icon', THRESHOLDS["icon"], HSV_PARAMETERS["icon"])

                if findings['icon']:
                    logger.debug(f'Found object. Finished step: {step}.')
                    step = Step.STEP_5

            if step == Step.STEP_5:
                logger.debug(f'Started step: {step}.')

                self.wait(TIME_AFTER_ICON_APPEARS)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_6

            if step == Step.STEP_6:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_7

            if step == Step.STEP_7:
                logger.debug(f'Started step: {step}.')

                self.wait(TIME_PAUSE_BEFORE_FISHING)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_8

            if step == Step.STEP_8:
                logger.debug(f'Started step: {step}.')

                findings = self.find('fishing_rod', THRESHOLDS["fishing_rod"], HSV_PARAMETERS["icon"])

                if findings['fishing_rod']:
                    logger.debug(f'Found object. Finished step: {step}.')
                    step = Step.STEP_9
                else:
                    logger.debug(f'Didnt find object. Finished step: {step}.')
                    step = Step.STEP_1
            
            if step == Step.STEP_9:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                findings = self.find(
                    ['arrow_blue', 'arrow_purple', 'arrow_yellow'],
                    [THRESHOLDS["arrow_blue"], THRESHOLDS["arrow_purple"], THRESHOLDS["arrow_yellow"]],
                    [HSV_PARAMETERS["arrow_blue"], HSV_PARAMETERS["arrow_purple"], HSV_PARAMETERS["arrow_yellow"]]
                )
                if any(findings['arrow_blue'], findings['arrow_purple'], findings['arrow_yellow']):
                    logger.debug(f'Found object. Finished step: {step}.')
                    step = Step.STEP_10
                else:
                    logger.debug(f'Didnt find object.')
                    self.wait(TIME_FISHING)

            if step == Step.STEP_10:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                findings = self.find(
                    ['arrow_blue', 'arrow_purple', 'arrow_yellow'],
                    [THRESHOLDS["arrow_blue"], THRESHOLDS["arrow_purple"], THRESHOLDS["arrow_yellow"]],
                    [HSV_PARAMETERS["arrow_blue"], HSV_PARAMETERS["arrow_purple"], HSV_PARAMETERS["arrow_yellow"]]
                )
                if findings['arrow_blue']:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING_ARROW_BLUE)
                elif findings['arrow_purple']:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING_ARROW_PURPLE)
                elif findings['arrow_yellow']:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING_ARROW_YELLOW)
                else:
                    logger.debug(f'Didnt find object. Finished step: {step}.')
                    step = Step.STEP_11

            if step == Step.STEP_11:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                findings = self.find('fishing_rod', THRESHOLDS["fishing_rod"], HSV_PARAMETERS["fishing_rod"])
                if findings['fishing_rod']:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING)
                else:
                    logger.debug(f'Didnt find object. Finished step: {step}.')
                    step = Step.STEP_1          
    
            # if cv.waitKey(1) == ord('q'):
            #     cv.destroyAllWindows()
            #     break

if __name__ == "__main__":
    window_capturer = WindowCapturer(WINDOW_NAME, WINDOW_BORDERS_OFFSET, WINDOW_TITLEBAR_OFFSET)
    hsv_filter = HsvFilter()
    finder = Finder(TEMPLATES)
    bot = Bot(window_capturer, finder, hsv_filter, DEBUG_MODE)

    bot.run()