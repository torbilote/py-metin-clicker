from app.screenshotter import Screenshotter
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.drawer import Drawer
from app.gui import GUI
import time
import pydirectinput
from cv2.typing import Rect, MatLike
from typing import Sequence
from numpy.typing import NDArray
import cv2 as cv
from typing import Optional, Literal
from loguru import logger as log


def make_screenshot(coordinates: dict[str, int]) -> NDArray | MatLike:
    screenshot = Screenshotter.make_screenshot(coordinates)
    log.debug(f'Made screenshot of {coordinates} coordinates.')
    return screenshot

def apply_filter_on_image(base_image: NDArray | MatLike, parameters: dict[str, int]) -> NDArray | MatLike:
    image_filtered = HsvFilter.apply_filter_on_image(base_image, parameters)
    log.debug(f'Applied filter on image with parameters: {parameters}.')
    return image_filtered

def add_template(template_name: str, template_path : str) -> None:
    Finder.add_template(template_name, template_path)
    log.debug(f'Added template {template_name} from {template_path}')

def find_template_on_image(template_name: str, base_image: NDArray | MatLike, threshold: float) -> Sequence[Rect]:
    findings = Finder.find_template_on_image(template_name, base_image, threshold)
    log.debug(f'Looked for template {template_name} with threshold {threshold}.')
    return findings

def show_rectangles(base_image: NDArray | MatLike, coordinates: Sequence[Rect]) -> None:
    Drawer.show_rectangles(base_image, coordinates)

def save_rectangles(base_image: NDArray | MatLike, coordinates: Sequence[Rect], file_prefix: str) -> None:
    Drawer.save_rectangles(base_image, coordinates, file_prefix)

def create_gui() -> None:
    GUI.create_gui()
    log.debug(f'Created GUI.')

def set_parameters_on_gui(parameters: dict[str, int]) -> None:
    GUI.set_parameters_on_gui(parameters)
    log.debug(f'Updated parameters on GUI. New parameters: {parameters}.')

def get_parameters_from_gui(parameter_type: Literal['hsv', 'threshold']) -> dict[str, int]:
    gui_parameters = GUI.get_parameters_from_gui(parameter_type)
    log.debug(f'Got parameters from GUI. Parameters: {gui_parameters}')
    return gui_parameters

def wait_seconds(wait_seconds: float) -> None:
    log.debug(f'Freezing for {wait_seconds}.')
    time.sleep(wait_seconds)
    log.debug(f'Freezing completed.')

def press_hotkey(key_name: str) -> None:
    time.sleep(0.01)
    pydirectinput.press(key_name)
    time.sleep(0.01)
    log.debug(f'Pressed {key_name} hotkey.')
    
def set_timer(timer: float) -> float:
    new_timer = timer if timer else time.time()
    if new_timer != timer:
        log.debug(f'Set timer for {timer} seconds.')
    return new_timer

def reset_timer() -> float:
    new_timer = 0.0
    log.debug(f'Reset timer.')
    return new_timer

def has_time_ended(start_time: float, time_limit: float) -> bool:
    current_time = time.time() - start_time
    time_ended = current_time >= time_limit
    log.debug(f'Has time ended: {time_ended}. Time difference: current_time: {current_time}, time_limit: {time_limit}.')
    return time_ended

def has_object_been_found(object_coordinates: Optional[Sequence[Rect]]) -> bool:
    object_been_found = len(object_coordinates) > 0
    log.debug(f'Has object been found: {object_been_found}.')
    return object_been_found

def load_image(image_path: str) -> NDArray | MatLike:
    image_loaded = cv.imread(image_path, cv.IMREAD_UNCHANGED)
    log.debug(f'Loaded image {image_path}.')
    return image_loaded