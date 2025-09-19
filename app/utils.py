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

def draw_rectangles(base_image: NDArray | MatLike, coordinates: Sequence[Rect]) -> None:
    Drawer.draw_rectangles(base_image, coordinates)

def create_gui() -> None:
    GUI.create_gui()

def set_parameters_on_gui(parameters: dict[str, int]) -> None:
    GUI.set_parameters_on_gui(parameters)

def get_parameters_from_gui(parameter_type: Literal['hsv', 'threshold']) -> dict[str, int]:
    return GUI.get_parameters_from_gui(parameter_type)

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

def load_image(image_path: str) -> NDArray | MatLike:
    return cv.imread(image_path, cv.IMREAD_UNCHANGED)