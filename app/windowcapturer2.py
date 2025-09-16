from mss import mss
from mss.base import MSSBase
from numpy.typing import NDArray
import numpy as np
from typing import Generator

class WindowCapturer:

    def __init__(self, coordinates: dict[str, int]) -> None:
        self.coordinates = {
            "top": coordinates.get("top", 0),
            "left": coordinates.get("left", 0),
            "width": coordinates.get("width", 800),
            "height": coordinates.get("height", 600),
        }

        self.handler = self._set_handler()

    def _set_handler(self) -> Generator[MSSBase, None, None]:
        with mss() as ss:
            while True:
                yield ss.grab(self.coordinates)

    def get_screenshot(self) -> NDArray:
        screenshot = next(self.handler)
        return np.array(screenshot)
        
    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_pixel_position_in_window(self, pixel_position_from_left: int, pixel_position_from_top: int) -> tuple[int, int]:
        return (pixel_position_from_left + self.coordinates['left'], pixel_position_from_top + self.coordinates['top'])