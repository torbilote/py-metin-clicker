from app.screenshotter import Screenshotter
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from app.constants import DEBUG_MODE, WINDOW_COORDINATES, TEMPLATE_BASE, TEMPLATE_ARROW_BLUE, TEMPLATE_ARROW_YELLOW, TEMPLATE_ARROW_PURPLE, TEMPLATE_FISHING_ROD, TEMPLATE_ICON, HOTKEYS, TIMERS, COUNTERS, STEPS

import cv2 as cv
import itertools
import time
from loguru import logger
import pydirectinput
from cv2.typing import Rect
from typing import Sequence
from numpy.typing import NDArray
from cv2.typing import MatLike

class Runner:
    screenshotter = Screenshotter(WINDOW_COORDINATES)
    finder = Finder([TEMPLATE_ARROW_BLUE, TEMPLATE_ARROW_PURPLE, TEMPLATE_ARROW_YELLOW, TEMPLATE_FISHING_ROD, TEMPLATE_ICON])

    def _wait_seconds(wait_seconds: float) -> None:
        interval_seconds = 0.1
        interval_miliseconds = int(interval_seconds * 1000)
        wait_miliseconds = int(wait_seconds * 1000)

        for miliseconds_left in range(wait_miliseconds, 0, -interval_miliseconds):
            time.sleep(interval_seconds)
            logger.debug(f'Waiting for {miliseconds_left/1000.0} more seconds..')

    def _press_hotkey(key_name: str) -> None:
        logger.debug(f'Pressing key: {key_name}..')
        time.sleep(0.01)
        pydirectinput.press(key_name)
        time.sleep(0.01)
        logger.debug(f'Key pressed.')

    @classmethod
    def _detect_template_on_screenshot(cls, templates: list[TEMPLATE_BASE]) -> dict[str, Sequence[Rect]]:
        findings = dict()
        
        screenshot_raw = cls.screenshotter.make_screenshot()

        for template in templates:
            screenshot_hsv = HsvFilter.apply_filter_on_image(screenshot_raw, template.HSV_PARAMETERS)
            findings[template.NAME] = cls.finder.find_template_on_image(template.NAME, screenshot_hsv, template.THRESHOLD)                                                                                                                     

        rectangles = itertools.chain(*findings.values())
        screenshot_with_rects = Drawer.draw_rectangles(screenshot_hsv, rectangles)

        for template_name, results in findings.items():
            if len(results) > 0:
                cv.imwrite(f'bot_screenshots/{template_name}.jpg', screenshot_with_rects)

        return findings

    @classmethod
    def start(cls) -> None:

        start_time_step_3 = None
        start_time_step_6 = None
        start_time_step_7 = None

        step = STEPS.STEP_1
        
        logger.debug('Started bot.')

        while True:
            
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
        
            if step == STEPS.STEP_1:
                logger.debug(f'Started step: {step}.')

                cls._wait_seconds(TIMERS.PAUSE_WHEN_NEW_ROUND_STARTS)

                step = STEPS.STEP_2

                logger.debug(f'Finished step: {step}.')

            if step == STEPS.STEP_2:
                logger.debug(f'Started step: {step}.')

                cls._press_hotkey(HOTKEYS.PICK_WORM)
                cls._wait_seconds(TIMERS.PAUSE_AFTER_WORM_IS_PICKED)
                cls._press_hotkey(HOTKEYS.ACTION)

                step = STEPS.STEP_3

                logger.debug(f'Finished step: {step}.')

            if step == STEPS.STEP_3:
                logger.debug(f'Started step: {step}.')

                start_time_step_3 = time.time() if not start_time_step_3 else start_time_step_3
                findings = cls._detect_template_on_screenshot([TEMPLATE_ICON])

                if len(findings['icon']) > 0:
                    step = STEPS.STEP_4
                    start_time_step_3 = None

                    logger.debug(f'Object found.')

                    cls._wait_seconds(TIMERS.PAUSE_AFTER_ICON_APPEARS)

                    logger.debug(f'Finished step: {step}.')
                elif time.time() - start_time_step_3 < TIMERS.WAITING_LIMIT_FOR_ICON_TO_APPEAR:
                    continue
                else:
                    step = STEPS.STEP_1
                    start_time_step_3 = None

                    logger.debug(f'Object not found in given time. Finished step: {step}.')

            if step == STEPS.STEP_4:
                logger.debug(f'Started step: {step}.')

                cls._press_hotkey(HOTKEYS.ACTION)

                step = STEPS.STEP_5

                logger.debug(f'Finished step: {step}.')

            if step == STEPS.STEP_5:
                logger.debug(f'Started step: {step}.')
                
                cls._wait_seconds(TIMERS.PAUSE_BEFORE_FISHING_ROD_APPEARS)
                findings = cls._detect_template_on_screenshot([TEMPLATE_FISHING_ROD])

                if len(findings['fishing_rod']) > 0:
                    step = STEPS.STEP_6

                    logger.debug(f'Object found.')

                    cls._wait_seconds(TIMERS.PAUSE_AFTER_FISHING_ROD_APPEARS)

                    logger.debug(f'Finished step: {step}.')
                else:
                    step = STEPS.STEP_1

                    logger.debug(f'Object not found. Finished step: {step}.')

            if step == STEPS.STEP_6:
                logger.debug(f'Started step: {step}.')

                start_time_step_6 = time.time() if not start_time_step_6 else start_time_step_6
                cls._press_hotkey(HOTKEYS.ACTION)
                findings = cls._detect_template_on_screenshot([TEMPLATE_ARROW_BLUE, TEMPLATE_ARROW_PURPLE, TEMPLATE_ARROW_YELLOW])

                if len(findings['arrow_blue']) > 0:
                    step = STEPS.STEP_7_BLUE
                    start_time_step_6 = None

                    logger.debug(f'Object found. Finished step: {step}.')
                if len(findings['arrow_purple']) > 0:
                    step = STEPS.STEP_7_PURPLE
                    start_time_step_6 = None

                    logger.debug(f'Object found. Finished step: {step}.')
                if len(findings['arrow_yellow']) > 0:
                    step = STEPS.STEP_7_YELLOW
                    start_time_step_6 = None

                    logger.debug(f'Object found. Finished step: {step}.')

                elif time.time() - start_time_step_6 < TIMERS.WAITING_LIMIT_FOR_FISHING:
                    cls._wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_GREEN_MODE)
                    continue

                else:
                    step = STEPS.STEP_1

                    logger.debug(f'Object not found in given time. Finished step: {step}.')

            if step == STEPS.STEP_7_BLUE:
                logger.debug(f'Started step: {step}.')

                start_time_step_7 = time.time() if not start_time_step_7 else start_time_step_7

                if time.time() - start_time_step_7 < TIMERS.WAITING_LIMIT_FOR_ACTIVE_MODE:
                    cls._press_hotkey(HOTKEYS.ACTION)
                    cls._wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_BLUE_MODE)
                    continue
                else:
                    step = STEPS.STEP_8
                    start_time_step_7 = None

                    logger.debug(f'Finished step: {step}.')
                

            if step == STEPS.STEP_7_PURPLE:
                logger.debug(f'Started step: {step}.')
                
                start_time_step_7 = time.time() if not start_time_step_7 else start_time_step_7

                if time.time() - start_time_step_7 < TIMERS.WAITING_LIMIT_FOR_ACTIVE_MODE:
                    cls._press_hotkey(HOTKEYS.ACTION)
                    cls._wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_PURPLE_MODE)
                    continue
                else:
                    step = STEPS.STEP_8
                    start_time_step_7 = None

                    logger.debug(f'Finished step: {step}.')


            if step == STEPS.STEP_7_YELLOW:
                logger.debug(f'Started step: {step}.')

                start_time_step_7 = time.time() if not start_time_step_7 else start_time_step_7

                if time.time() - start_time_step_7 < TIMERS.WAITING_LIMIT_FOR_ACTIVE_MODE:
                    cls._press_hotkey(HOTKEYS.ACTION)
                    cls._wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_YELLOW_MODE)
                    continue
                else:
                    step = STEPS.STEP_8
                    start_time_step_7 = None

                    logger.debug(f'Finished step: {step}.')

            if step == STEPS.STEP_8:
                logger.debug(f'Started step: {step}.')

                findings = cls._detect_template_on_screenshot([TEMPLATE_FISHING_ROD])

                if len(findings['fishing_rod']) > 0:
                    cls._press_hotkey(HOTKEYS.ACTION)
                    cls._wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_GREEN_MODE)
                    continue
                else:
                    step = STEPS.STEP_1

                    logger.debug(f'Object not found. End of the loop. Finished step: {step}.')