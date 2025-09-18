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
from typing import Optional

def make_screenshot(coordinates: dict[str, int]) -> NDArray | MatLike:
    return Screenshotter.make_screenshot(coordinates)

def save_screenshot(screenshot: NDArray | MatLike, file_path: str) -> None:
    Screenshotter.save_screenshot(screenshot, file_path)

def draw_rectangles(base_image: NDArray | MatLike, rectangles: Sequence[Rect]) -> None:
    Drawer.draw_rectangles(base_image, rectangles)

def get_rectangles(base_image: NDArray | MatLike, rectangles: Sequence[Rect]) -> NDArray | MatLike:
    return Drawer.get_rectangles(base_image, rectangles)

def apply_filter_on_image(base_image: NDArray | MatLike, parameters: dict[str, int]) -> NDArray | MatLike:
    return HsvFilter.apply_filter_on_image(base_image, parameters)

def find_template_on_image(template_name: str, base_image: NDArray | MatLike, threshold: float) -> Sequence[Rect]:
    return Finder.find_template_on_image(template_name, base_image, threshold)

def wait_seconds(wait_seconds: float) -> None:
    time.sleep(wait_seconds)

def press_hotkey(key_name: str) -> None:
    time.sleep(0.01)
    pydirectinput.press(key_name)
    time.sleep(0.01)
    
def set_timer(timer: float) -> float:
    return timer if timer else time.time()

def reset_timer() -> float:
    return 0.0

def has_time_ended(start_time: float, time_limit: float) -> bool:
    return time.time() - start_time >= time_limit

def has_object_been_found(object_coordinates: Optional[Sequence[Rect]]) -> bool:
    return len(object_coordinates) > 0

def main() -> None:
    start_time_3: float = 0.0
    start_time_6: float = 0.0
    start_time_7: float = 0.0

    step = STEPS.STEP_1

    while True:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

        if step == STEPS.STEP_1:
            wait_seconds(TIMERS.PAUSE_WHEN_NEW_ROUND_STARTS)
            step = STEPS.STEP_2

        if step == STEPS.STEP_2:
            press_hotkey(HOTKEYS.PICK_WORM)
            wait_seconds(TIMERS.PAUSE_AFTER_WORM_IS_PICKED)
            press_hotkey(HOTKEYS.ACTION)
            step = STEPS.STEP_3

        if step == STEPS.STEP_3:
            start_time_3 = set_timer(start_time_3)
            findings = find_template_on_image(TEMPLATE_ICON)

            if has_object_been_found(findings):
                wait_seconds(TIMERS.PAUSE_AFTER_ICON_APPEARS)
                start_time_3 = reset_timer()
                step = STEPS.STEP_4
            elif not has_time_ended(start_time_3, TIMERS.WAITING_LIMIT_FOR_ICON_TO_APPEAR):
                continue
            else:
                start_time_3 = reset_timer()
                step = STEPS.STEP_1

        if step == STEPS.STEP_4:
            press_hotkey(HOTKEYS.ACTION)
            step = STEPS.STEP_5

        if step == STEPS.STEP_5:            
            wait_seconds(TIMERS.PAUSE_BEFORE_FISHING_ROD_APPEARS)
            findings = find_template_on_image(TEMPLATE_FISHING_ROD)

            if has_object_been_found(findings):
                wait_seconds(TIMERS.PAUSE_AFTER_FISHING_ROD_APPEARS)
                step = STEPS.STEP_6
            else:
                step = STEPS.STEP_1

        if step == STEPS.STEP_6:
            start_time_6 = set_timer(start_time_6)
            press_hotkey(HOTKEYS.ACTION)

            findings_arrow_blue = find_template_on_image(TEMPLATE_ARROW_BLUE)
            if has_object_been_found(findings_arrow_blue):
                step = STEPS.STEP_7_BLUE
                start_time_6 = reset_timer()
                continue

            findings_arrow_purple = find_template_on_image(TEMPLATE_ARROW_PURPLE)
            if has_object_been_found(findings_arrow_purple):
                step = STEPS.STEP_7_PURPLE
                start_time_6 = reset_timer()
                continue

            findings_arrow_yellow = find_template_on_image(TEMPLATE_ARROW_YELLOW)
            if has_object_been_found(findings_arrow_yellow):
                step = STEPS.STEP_7_YELLOW
                start_time_6 = reset_timer()
                continue

            if not has_time_ended(start_time_6, TIMERS.WAITING_LIMIT_FOR_FISHING):
                wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_GREEN_MODE)
                continue
            else:
                step = STEPS.STEP_1

        if step in (STEPS.STEP_7_BLUE, STEPS.STEP_7_PURPLE, STEPS.STEP_7_YELLOW):
            start_time_7 = set_timer(start_time_7)

            if has_time_ended(start_time_7, TIMERS.WAITING_LIMIT_FOR_ACTIVE_MODE):
                press_hotkey(HOTKEYS.ACTION)

                if step == STEPS.STEP_7_BLUE:
                    wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_BLUE_MODE)
                elif step == STEPS.STEP_7_PURPLE:
                    wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_PURPLE_MODE)
                elif step == STEPS.STEP_7_YELLOW:
                    wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_YELLOW_MODE)

                continue
            else:
                step = STEPS.STEP_8
                start_time_7 = reset_timer()

        if step == STEPS.STEP_8:
            findings = find_template_on_image(TEMPLATE_FISHING_ROD)

            if has_object_been_found(findings):
                press_hotkey(HOTKEYS.ACTION)
                wait_seconds(TIMERS.INTERVAL_WHEN_FISHING_GREEN_MODE)
                continue
            else:
                step = STEPS.STEP_1


if __name__ == "__main__":
    main()