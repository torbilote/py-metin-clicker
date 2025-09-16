from mss import mss
from mss.base import MSSBase
from numpy.typing import NDArray
import numpy as np
from typing import Generator
from cv2.typing import MatLike
import cv2 as cv

class Screenshot:

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
    
    def make_screenshot(self) -> NDArray:
        screenshot = next(self.handler)
        return np.array(screenshot)
    
    def save_screenshot(self, image: NDArray | MatLike, path: str) -> None:
        cv.imwrite(path, image)