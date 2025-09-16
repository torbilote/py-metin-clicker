from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from app.windowcapturer2 import WindowCapturer
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

DEBUG_MODE = False

WINDOW_COORDINATES = {"top": 0, "left": 0, "width": 800, "height": 600}

HSV_PARAMETERS = {
    "arrow_blue"    : {'hMin': 84, 'sMin': 20, 'vMin': 54, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0},
    "arrow_purple"  : {'hMin': 84, 'sMin': 20, 'vMin': 54, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0},
    "arrow_yellow"  : {'hMin': 0, 'sMin': 0, 'vMin': 79, 'hMax': 36, 'sMax': 114, 'vMax': 255, 'sAdd': 45, 'sSub': 0, 'vAdd': 0, 'vSub': 0},
    "fishing_rod"   : {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0},
    "icon"          : {'hMin': 0, 'sMin': 0, 'vMin': 143, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 190, 'vAdd': 0, 'vSub': 0},
}

TEMPLATES = {
    "arrow_blue"    : "templates/arrow_blue2.jpg",
    "arrow_purple"  : "templates/arrow_purple2.jpg",
    "arrow_yellow"  : "templates/arrow_yellow2.jpg",
    "fishing_rod"   : "templates/fishing_rod.jpg",
    "icon"          : "templates/icon2.jpg",
}

THRESHOLDS = {
    "arrow_blue"    : 0.9,
    "arrow_purple"  : 0.9,
    "arrow_yellow"  : 0.5,
    "fishing_rod"   : 0.5,
    "icon"          : 0.6,
}

TIME_BEGINNING              = 5000                  # miliseconds
TIME_AFTER_ICON_APPEARS     = 2500                  # miliseconds
TIME_PAUSE_BEFORE_FISHING_ROD_APPEARS = 1000        # miliseconds
TIME_PAUSE_BEFORE_FISHING   = 4000                  # miliseconds
TIME_FISHING                = 0                   # miliseconds
TIME_FISHING_ARROW_BLUE     = TIME_FISHING * 2      # miliseconds
TIME_FISHING_ARROW_PURPLE   = TIME_FISHING / 2      # miliseconds
TIME_FISHING_ARROW_YELLOW   = TIME_FISHING / 4      # miliseconds

KEY_WORM    = '2'
KEY_FISHING = 'space'

class Step(Enum):
    STEP_1: int = 1 # wait
    STEP_2: int = 2 # press '2'
    STEP_3: int = 3 # press 'space' and wait
    STEP_4: int = 4 # find 'icon'
    STEP_5: int = 5 # wait 
    STEP_6: int = 6 # press 'space'
    STEP_7: int = 7 # find 'fishing_rod'
    STEP_8: int = 8 
    STEP_9: int = 9 # press 'space' and find 'arrow'
    STEP_10: int = 10 # press 'space' and find 'arrow'
    STEP_11: int = 11 # press 'space' and find 'fishing_rod'

class Bot:
    def __init__(self, window_capturer: WindowCapturer, finder: Finder, hsv_filter: HsvFilter, debug_mode: bool) -> None:
        self.debug_mode = debug_mode
        
        self.window_capturer = window_capturer
        self.finder = finder
        self.hsv_filter = hsv_filter

    def wait(self, miliseconds: int) -> None:
        logger.debug(f'Waiting  {(miliseconds)/1000.0} seconds..')
        time.sleep(miliseconds/1000.0)

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

            screenshot_with_rects = Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)
            
            for template in results:
                if len(results[template]) > 0:
                    cv.imwrite(f'bot_screenshots/{template}.jpg', screenshot_with_rects)

        return results


    def run(self) -> None:
        # if self.debug_mode:
        #     WindowCapturer.list_window_names()

        step = Step.STEP_1
        logger.debug('Started bot.')

        while True:

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

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
                logger.debug(findings)

                if len(findings['icon']) > 0:
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

                self.wait(TIME_PAUSE_BEFORE_FISHING_ROD_APPEARS)

                findings = self.find('fishing_rod', THRESHOLDS["fishing_rod"], HSV_PARAMETERS["fishing_rod"])
                logger.debug(findings)

                if len(findings['fishing_rod']) > 0:
                    logger.debug(f'Found object. Finished step: {step}.')
                    step = Step.STEP_8
                else:
                    logger.debug(f'Didnt find object. Finished step: {step}.')
                    step = Step.STEP_1

            if step == Step.STEP_8:
                logger.debug(f'Started step: {step}.')

                self.wait(TIME_PAUSE_BEFORE_FISHING)

                logger.debug(f'Finished step: {step}.')
                step = Step.STEP_9

            if step == Step.STEP_9:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                findings = self.find(
                    ['arrow_blue', 'arrow_purple', 'arrow_yellow'],
                    [THRESHOLDS["arrow_blue"], THRESHOLDS["arrow_purple"], THRESHOLDS["arrow_yellow"]],
                    [HSV_PARAMETERS["arrow_blue"], HSV_PARAMETERS["arrow_purple"], HSV_PARAMETERS["arrow_yellow"]]
                )
                logger.debug(findings)
                
                if len(findings['arrow_blue']) > 0 or len(findings['arrow_purple']) > 0 or len(findings['arrow_yellow']) > 0:
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
                logger.debug(findings)

                if len(findings['arrow_blue']) > 0:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING_ARROW_BLUE)
                elif len(findings['arrow_purple']) > 0:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING_ARROW_PURPLE)
                elif len(findings['arrow_yellow']) > 0:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING_ARROW_YELLOW)
                else:
                    logger.debug(f'Didnt find object. Finished step: {step}.')
                    step = Step.STEP_11

            if step == Step.STEP_11:
                logger.debug(f'Started step: {step}.')

                self.press(KEY_FISHING)

                findings = self.find('fishing_rod', THRESHOLDS["fishing_rod"], HSV_PARAMETERS["fishing_rod"])
                logger.debug(findings)

                if len(findings['fishing_rod']) > 0:
                    logger.debug(f'Found object.')
                    self.wait(TIME_FISHING)
                else:
                    logger.debug(f'Didnt find object. Finished step: {step}.')
                    step = Step.STEP_1          

if __name__ == "__main__":
    window_capturer = WindowCapturer(WINDOW_COORDINATES)
    hsv_filter = HsvFilter()
    finder = Finder(TEMPLATES)
    bot = Bot(window_capturer, finder, hsv_filter, DEBUG_MODE)

    bot.run()