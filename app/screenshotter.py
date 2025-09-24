from mss import mss
from mss.screenshot import ScreenShot
from numpy.typing import NDArray
import numpy as np
from typing import Generator, Optional
from cv2.typing import MatLike

class Screenshotter:
    handler: Optional[Generator[ScreenShot, None, None]] = None

    def _set_handler(coordinates) -> Generator[ScreenShot, None, None]:
        with mss() as ss:
            while True:
                yield ss.grab(coordinates)
    
    @classmethod
    def make_screenshot(cls, coordinates: dict[str, int]) -> NDArray | MatLike:
        if not cls.handler:
            cls.handler = cls._set_handler(coordinates)

        screenshot = next(cls.handler)
        return np.array(screenshot)