from app.screenshotter import Screenshotter
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from app import constants as c

import cv2 as cv
import time
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

def apply_filter_on_image(base_image: NDArray | MatLike, parameters: dict[str, int]) -> NDArray | MatLike:
    return HsvFilter.apply_filter_on_image(base_image, parameters)

def add_template(template_name: str, template_path : str) -> None:
    Finder.add_template(template_name, template_path)

def find_template_on_image(template_name: str, base_image: NDArray | MatLike, threshold: float) -> Sequence[Rect]:
    return Finder.find_template_on_image(template_name, base_image, threshold)

def draw_rectangles(base_image: NDArray | MatLike, rectangles: Sequence[Rect]) -> None:
    Drawer.draw_rectangles(base_image, rectangles)

def get_rectangles(base_image: NDArray | MatLike, rectangles: Sequence[Rect]) -> NDArray | MatLike:
    return Drawer.get_rectangles(base_image, rectangles)

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
    Finder.add_template(c.TEMPLATE_ARROW_BLUE_NAME, c.TEMPLATE_ARROW_BLUE_IMAGE_PATH)
    Finder.add_template(c.TEMPLATE_ARROW_PURPLE_NAME, c.TEMPLATE_ARROW_PURPLE_IMAGE_PATH)
    Finder.add_template(c.TEMPLATE_ARROW_YELLOW_NAME, c.TEMPLATE_ARROW_YELLOW_IMAGE_PATH)
    Finder.add_template(c.TEMPLATE_FISHING_ROD_NAME, c.TEMPLATE_FISHING_ROD_IMAGE_PATH)
    Finder.add_template(c.TEMPLATE_ICON_NAME, c.TEMPLATE_ICON_IMAGE_PATH)

    step = c.STEP_1

    start_time_3: float = 0.0
    start_time_6: float = 0.0
    start_time_7: float = 0.0

    while True:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

        if step == c.STEP_1:
            wait_seconds(c.TIMER_PAUSE_WHEN_NEW_ROUND_STARTS)
            step = c.STEP_2

        if step == c.STEP_2:
            press_hotkey(c.HOTKEY_PICK_WORM)
            wait_seconds(c.TIMER_PAUSE_AFTER_WORM_IS_PICKED)
            press_hotkey(c.HOTKEY_ACTION)
            step = c.STEP_3

        if step == c.STEP_3:
            start_time_3 = set_timer(start_time_3)
            screenshot_raw = make_screenshot(c.WINDOW_COORDINATES)
            screenshot_hsv = apply_filter_on_image(screenshot_raw, c.TEMPLATE_ICON_HSV_PARAMETERS)
            findings = find_template_on_image(c.TEMPLATE_ICON_NAME, screenshot_hsv, c.TEMPLATE_ICON_THRESHOLD)

            if has_object_been_found(findings):
                wait_seconds(c.TIMER_PAUSE_AFTER_ICON_APPEARS)
                start_time_3 = reset_timer()
                step = c.STEP_4
            elif not has_time_ended(start_time_3, c.TIMER_WAITING_LIMIT_FOR_ICON_TO_APPEAR):
                continue
            else:
                start_time_3 = reset_timer()
                step = c.STEP_1

        if step == c.STEP_4:
            press_hotkey(c.HOTKEY_ACTION)
            step = c.STEP_5

        if step == c.STEP_5:            
            wait_seconds(c.TIMER_PAUSE_BEFORE_FISHING_ROD_APPEARS)
            screenshot_raw = make_screenshot(c.WINDOW_COORDINATES)
            screenshot_hsv = apply_filter_on_image(screenshot_raw, c.TEMPLATE_FISHING_ROD_HSV_PARAMETERS)
            findings = find_template_on_image(c.TEMPLATE_FISHING_ROD_NAME, screenshot_hsv, c.TEMPLATE_FISHING_ROD_THRESHOLD)

            if has_object_been_found(findings):
                wait_seconds(c.TIMER_PAUSE_AFTER_FISHING_ROD_APPEARS)
                step = c.STEP_6
            else:
                step = c.STEP_1

        if step == c.STEP_6:
            start_time_6 = set_timer(start_time_6)
            press_hotkey(c.HOTKEY_ACTION)
            screenshot_raw = make_screenshot(c.WINDOW_COORDINATES)
            
            screenshot_hsv_arrow_blue = apply_filter_on_image(screenshot_raw, c.TEMPLATE_ARROW_BLUE_HSV_PARAMETERS)
            findings_arrow_blue = find_template_on_image(c.TEMPLATE_ARROW_BLUE_NAME, screenshot_hsv_arrow_blue, c.TEMPLATE_ARROW_BLUE_THRESHOLD)
            if has_object_been_found(findings_arrow_blue):
                step = c.STEP_7_BLUE
                start_time_6 = reset_timer()
                continue
            
            screenshot_hsv_arrow_purple = apply_filter_on_image(screenshot_raw, c.TEMPLATE_ARROW_PURPLE_HSV_PARAMETERS)
            findings_arrow_purple = find_template_on_image(c.TEMPLATE_ARROW_PURPLE_NAME, screenshot_hsv_arrow_purple, c.TEMPLATE_ARROW_PURPLE_THRESHOLD)
            if has_object_been_found(findings_arrow_purple):
                step = c.STEP_7_PURPLE
                start_time_6 = reset_timer()
                continue

            screenshot_hsv_arrow_yellow = apply_filter_on_image(screenshot_raw, c.TEMPLATE_ARROW_YELLOW_HSV_PARAMETERS)
            findings_arrow_yellow = find_template_on_image(c.TEMPLATE_ARROW_YELLOW_NAME, screenshot_hsv_arrow_yellow, c.TEMPLATE_ARROW_YELLOW_THRESHOLD)
            if has_object_been_found(findings_arrow_yellow):
                step = c.STEP_7_YELLOW
                start_time_6 = reset_timer()
                continue

            if not has_time_ended(start_time_6, c.TIMER_WAITING_LIMIT_FOR_FISHING):
                wait_seconds(c.TIMER_INTERVAL_WHEN_FISHING_GREEN_MODE)
                continue
            else:
                step = c.STEP_1

        if step in (c.STEP_7_BLUE, c.STEP_7_PURPLE, c.STEP_7_YELLOW):
            start_time_7 = set_timer(start_time_7)

            if has_time_ended(start_time_7, c.TIMER_WAITING_LIMIT_FOR_ACTIVE_MODE):
                press_hotkey(c.HOTKEY_ACTION)

                if step == c.STEP_7_BLUE:
                    wait_seconds(c.TIMER_INTERVAL_WHEN_FISHING_BLUE_MODE)
                elif step == c.STEP_7_PURPLE:
                    wait_seconds(c.TIMER_INTERVAL_WHEN_FISHING_PURPLE_MODE)
                elif step == c.STEP_7_YELLOW:
                    wait_seconds(c.TIMER_INTERVAL_WHEN_FISHING_YELLOW_MODE)

                continue
            else:
                step = c.STEP_8
                start_time_7 = reset_timer()

        if step == c.STEP_8:
            screenshot_raw = make_screenshot(c.WINDOW_COORDINATES)
            screenshot_hsv = apply_filter_on_image(screenshot_raw, c.TEMPLATE_FISHING_ROD_HSV_PARAMETERS)
            findings = find_template_on_image(c.TEMPLATE_FISHING_ROD_NAME, screenshot_hsv, c.TEMPLATE_FISHING_ROD_THRESHOLD)

            if has_object_been_found(findings):
                press_hotkey(c.HOTKEY_ACTION)
                wait_seconds(c.TIMER_INTERVAL_WHEN_FISHING_GREEN_MODE)
                continue
            else:
                step = c.STEP_1


if __name__ == "__main__":
    main()