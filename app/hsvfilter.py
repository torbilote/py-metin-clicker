import cv2 as cv
import numpy as np
from typing import Sequence
from numpy.typing import NDArray
from cv2.typing import MatLike

# custom data structure to hold the state of an HSV filter
class HsvFilter:

    def __init__(
            self,
            gui: bool = False,
            hMin: int = 0,
            sMin: int = 0,
            vMin: int = 0,
            hMax: int = 179,
            sMax: int = 255,
            vMax: int = 255,
            sAdd: int = 0,
            sSub: int = 0,
            vAdd: int = 0,
            vSub: int = 0,
        ) -> None:

        self.TRACKBAR_WINDOW = "Trackbars"

        self.gui = gui
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub

        if self.gui:
            self._create_control_gui()
    
    # create gui window with controls for adjusting arguments in real-time
    def _create_control_gui(self) -> None:
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.getTrackbarPos
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, self._empty_callback)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, self._empty_callback)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, self._empty_callback)

        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMin', self.TRACKBAR_WINDOW, self.hMin)
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, self.hMax)
        cv.setTrackbarPos('SMin', self.TRACKBAR_WINDOW, self.sMin)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, self.sMax)
        cv.setTrackbarPos('VMin', self.TRACKBAR_WINDOW, self.vMin)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, self.vMax)

        cv.setTrackbarPos('SAdd', self.TRACKBAR_WINDOW, self.sAdd)
        cv.setTrackbarPos('SSub', self.TRACKBAR_WINDOW, self.sSub)
        cv.setTrackbarPos('VAdd', self.TRACKBAR_WINDOW, self.vAdd)
        cv.setTrackbarPos('VSub', self.TRACKBAR_WINDOW, self.vSub)

    # required callback. we'll be using getTrackbarPos() to do lookups
    # instead of using the callback.
    def _empty_callback(self, _) -> None:
        ...
    
    def _get_hsv_filter_from_controls(self) -> None:
        # Get current positions of all trackbars
        self.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        self.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        self.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        self.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        self.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        self.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        self.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        self.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        self.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        self.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
    
    # given an image and an HSV filter, apply the filter and return the resulting image.
    # if a filter is not supplied, the control GUI trackbars will be used
    def apply_hsv_filter(self, original_image: NDArray | MatLike) -> NDArray | MatLike:
        # convert image to HSV
        hsv_image = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if self.gui:
            self._get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv_image)
        s = self._shift_channel(s, self.sAdd)
        s = self._shift_channel(s, -self.sSub)
        v = self._shift_channel(v, self.vAdd)
        v = self._shift_channel(v, -self.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([self.hMin, self.sMin, self.vMin])
        upper = np.array([self.hMax, self.sMax, self.vMax])

        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        processed_image = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return processed_image

    # apply adjustments to an HSV channel
    # https://stackoverflow.com/questions/49697363/shifting-hsv-pixel-values-in-python-using-numpy
    def _shift_channel(self, c: Sequence[MatLike], amount: int) -> Sequence[MatLike]:
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