import cv2 as cv
import numpy as np
from typing import Sequence
from numpy.typing import NDArray
from cv2.typing import MatLike

class HsvFilter:
    def __init__(self) -> None:
        ...

    @staticmethod
    def apply_filter_on_image(base_image: NDArray | MatLike, parameters: dict[str, int]) -> NDArray | MatLike:
        hsv_image = cv.cvtColor(base_image, cv.COLOR_BGR2HSV)

        h, s, v = cv.split(hsv_image)
        s = HsvFilter._shift_channel(s, parameters['sAdd'])
        s = HsvFilter._shift_channel(s, -parameters['sSub'])
        v = HsvFilter._shift_channel(v, parameters['vAdd'])
        v = HsvFilter._shift_channel(v, -parameters['vSub'])
        hsv = cv.merge([h, s, v])

        lower = np.array([parameters['hMin'], parameters['sMin'], parameters['vMin']])
        upper = np.array([parameters['hMax'], parameters['sMax'], parameters['vMax']])

        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        processed_image = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return processed_image

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    @staticmethod
    def _shift_channel(c: Sequence[MatLike], amount: int) -> Sequence[MatLike]:
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c