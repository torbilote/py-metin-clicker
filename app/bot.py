from app.drawer import Drawer
from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
import cv2 as cv
import itertools
from numpy.typing import NDArray
from enum import Enum
import time
from loguru import logger
import pydirectinput


class Status(Enum):
    STOPPED: int = 1
    RUNNING: int = 2

class Step(Enum):
    STEP_1: int = 1 # make screenshot
    STEP_2: int = 2 # apply hsv filter

    STEP_3: int = 3 # 
    STEP_4: int = 4
    STEP_5: int = 5
    STEP_6: int = 6
    STEP_7: int = 7


class Bot:
    def __init__(self, window_capturer: WindowCapturer, finder: Finder, hsv_filter: HsvFilter, debug_mode: bool) -> None:
        self.window_capturer = window_capturer
        self.finder = finder
        self.hsv_filter = hsv_filter
        self.debug_mode = debug_mode

        self.bot_status = Status.STOPPED
        self.bot_stage = Step.STEP_1

        self.screenshot_raw = None
        self.screenshot_hsv = None

    def run(self) -> None:
            # if self.bot_stage == Step.STEP_2:
            #     self.screenshot_hsv = self.hsv_filter.apply_hsv_filter(self.screenshot)
            #     self.bot_stage = Step.STEP_3
        logger.debug(f"Initializing...")
        if self.debug_mode:
            WindowCapturer.list_window_names()

        state = 1
        step = 1
        logger.debug(f"Logged all windows...")
        while state:
            clicking_speed = 0.3
            # step 1 - wait 5 seconds
            if step == 1:
                logger.debug(f"Step {step} started.")
                for i in range(5):
                    logger.info(f'Staring in {5 - i}')
                    time.sleep(1)
                step = step + 1
                logger.debug(f"Step {step} completed.")

            # step 2 - press '2' key and wait 1 seconds.
            if step == 2:
                logger.debug(f"Step {step} started.")
                pydirectinput.press('2')
                time.sleep(1)
                step = step + 1
                logger.debug(f"Step {step} completed.")

            # step 3 - press 'space' key and wait 0.5 seconds.
            if step == 3:
                logger.debug(f"Step {step} started.")
                pydirectinput.press('space')
                time.sleep(0.5)
                step = step + 1
                logger.debug(f"Step {step} completed.")

            # step 4 - look for the icon appearing.
            if step == 4:
                logger.debug(f"Step {step} started.")
                screenshot_raw = self.window_capturer.get_screenshot()
                # screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)

                icon_finding_results = self.finder.find_images(['icon'], screenshot_hsv, threshold=0.9)

                if self.debug_mode:
                    print(icon_finding_results)
                    templates_rectangles = itertools.chain(*icon_finding_results.values())
                    Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)
                
                if icon_finding_results['icon']:
                    step = step + 1
                    logger.debug(f"Step {step} completed.")

             # step 5 - look for the icon disappearing.
            if step == 5:
                logger.debug(f"Step {step} started.")
                screenshot_raw = self.window_capturer.get_screenshot()
                # screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)

                icon_finding_results = self.finder.find_images(['icon'], screenshot_hsv, threshold=0.9)

                if self.debug_mode:
                    print(icon_finding_results)
                    templates_rectangles = itertools.chain(*icon_finding_results.values())
                    Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)

                if not icon_finding_results['icon']:
                    step = step + 1
                    logger.debug(f"Step {step} completed.")

            # step 6 - press 'space' key and wait 5 seconds.
            if step == 6:
                logger.debug(f"Step {step} started.")
                pydirectinput.press('space')
                time.sleep(5)
                step = step + 1
                logger.debug(f"Step {step} completed.")

            # step 7 - look for the fishing rod appearing.
            if step == 7:
                logger.debug(f"Step {step} started.")
                screenshot_raw = self.window_capturer.get_screenshot()
                # screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)

                icon_finding_results = self.finder.find_images(['fishing_rod'], screenshot_hsv, threshold=0.9)

                if self.debug_mode:
                    print(icon_finding_results)
                    templates_rectangles = itertools.chain(*icon_finding_results.values())
                    Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)

                if icon_finding_results['fishing_rod']:
                    step = step + 1
                    logger.debug(f"Step {step} completed.")
                else:
                    step=1
                    logger.debug(f"Step {step} completed and starting over.")

            # step 8 - press 'space' key and look for arrows.
            if step == 8:
                logger.debug(f"Step {step} started.")
                pydirectinput.press('space')

                screenshot_raw = self.window_capturer.get_screenshot()
                # screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)

                icon_finding_results = self.finder.find_images(['arrow_blue', 'arrow_purple', 'arrow_yellow'], screenshot_hsv, threshold=0.9)

                if self.debug_mode:
                    print(icon_finding_results)
                    templates_rectangles = itertools.chain(*icon_finding_results.values())
                    Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)

                time.sleep(clicking_speed)

                if any(icon_finding_results['arrow_blue'],
                       icon_finding_results['arrow_purple'],
                       icon_finding_results['arrow_yellow']):
                    step = step + 1
                    logger.debug(f"Step {step} completed.")

            # step 9 - press space with the speed according to the type of arrow.
            if step == 9:
                logger.debug(f"Step {step} started.")
                pydirectinput.press('space')

                screenshot_raw = self.window_capturer.get_screenshot()
                # screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)

                icon_finding_results = self.finder.find_images(['arrow_blue', 'arrow_purple', 'arrow_yellow'], screenshot_hsv, threshold=0.9)

                if self.debug_mode:
                    print(icon_finding_results)
                    templates_rectangles = itertools.chain(*icon_finding_results.values())
                    Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)

                if icon_finding_results['arrow_blue']:
                    time.sleep(clicking_speed*2)
                    continue
                if icon_finding_results['arrow_purple']:
                    time.sleep(clicking_speed/2)
                    continue
                if icon_finding_results['arrow_yellow']:
                    time.sleep(clicking_speed/4)
                    continue
                else:
                    step = step + 1
                    logger.debug(f"Step {step} completed.")

            # step 10 - press 'space' until the fishing rod disappears.
            if step == 10:
                logger.debug(f"Step {step} started.")
                pydirectinput.press('space')

                screenshot_raw = self.window_capturer.get_screenshot()
                # screenshot = cv.imread('img/test_arrow_purple.jpg', cv.IMREAD_UNCHANGED)

                screenshot_hsv = self.hsv_filter.apply_hsv_filter(screenshot_raw)

                icon_finding_results = self.finder.find_images(['fishing_rod'], screenshot_hsv, threshold=0.9)

                if self.debug_mode:
                    print(icon_finding_results)
                    templates_rectangles = itertools.chain(*icon_finding_results.values())
                    Drawer.draw_rectangles(screenshot_hsv, templates_rectangles)

                time.sleep(clicking_speed)

                if not icon_finding_results['fishing_rod']:
                    step = step + 1
                    logger.debug(f"Step {step} completed.")

            # step 11 - wait 5 seconds and start the loop again.
            if step == 11:
                logger.debug(f"Step {step} started.")
                time.sleep(5)
                step=1
                logger.debug(f"Step {step} completed and starting over.")
            
    

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break



        if self.debug_mode:
            print('Latest HSV Filter Configuration:\n',
                f"hMin: {self.hsv_filter.hsv_parameters['hMin']}\n",
                f"sMin: {self.hsv_filter.hsv_parameters['sMin']}\n",
                f"vMin: {self.hsv_filter.hsv_parameters['vMin']}\n",
                f"hMax: {self.hsv_filter.hsv_parameters['hMax']}\n",
                f"sMax: {self.hsv_filter.hsv_parameters['sMax']}\n",
                f"vMax: {self.hsv_filter.hsv_parameters['vMax']}\n",
                f"sAdd: {self.hsv_filter.hsv_parameters['sAdd']}\n",
                f"sSub: {self.hsv_filter.hsv_parameters['sSub']}\n",
                f"vAdd: {self.hsv_filter.hsv_parameters['vAdd']}\n",
                f"vSub: {self.hsv_filter.hsv_parameters['vSub']}\n",
                )