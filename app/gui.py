import cv2 as cv
from typing import Literal
class GUI:
    window_name: str = "Trackbars"
    
    @classmethod
    def create_gui(cls) -> None:
        cv.namedWindow(cls.window_name, cv.WINDOW_AUTOSIZE)

        cv.createTrackbar('hMin', cls.window_name, 0, 179, lambda x: None)
        cv.setTrackbarMin('hMin', cls.window_name, 0)
        cv.setTrackbarMax('hMin', cls.window_name, 179)

        cv.createTrackbar('sMin', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('sMin', cls.window_name, 0)
        cv.setTrackbarMax('sMin', cls.window_name, 255)

        cv.createTrackbar('vMin', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('vMin', cls.window_name, 0)
        cv.setTrackbarMax('vMin', cls.window_name, 255)

        cv.createTrackbar('hMax', cls.window_name, 0, 179, lambda x: None)
        cv.setTrackbarMin('hMax', cls.window_name, 0)
        cv.setTrackbarMax('hMax', cls.window_name, 179)

        cv.createTrackbar('sMax', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('sMax', cls.window_name, 0)
        cv.setTrackbarMax('sMax', cls.window_name, 255)

        cv.createTrackbar('vMax', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('vMax', cls.window_name, 0)
        cv.setTrackbarMax('vMax', cls.window_name, 255)

        cv.createTrackbar('sAdd', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('sAdd', cls.window_name, 0)
        cv.setTrackbarMax('sAdd', cls.window_name, 255)

        cv.createTrackbar('sSub', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('sSub', cls.window_name, 0)
        cv.setTrackbarMax('sSub', cls.window_name, 255)

        cv.createTrackbar('vAdd', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('vAdd', cls.window_name, 0)
        cv.setTrackbarMax('vAdd', cls.window_name, 255)

        cv.createTrackbar('vSub', cls.window_name, 0, 255, lambda x: None)
        cv.setTrackbarMin('vSub', cls.window_name, 0)
        cv.setTrackbarMax('vSub', cls.window_name, 255)
        
        cv.createTrackbar('threshold', cls.window_name, 50, 100, lambda x: None) 
        cv.setTrackbarMin('threshold', cls.window_name, 25)
        cv.setTrackbarMax('threshold', cls.window_name, 100)
    
    @classmethod
    def set_parameters_on_gui(cls, parameters: dict[str, int]) -> None:
        for name, value in parameters.items():
            if name == 'threshold':
                cv.setTrackbarPos(name, cls.window_name, int(value * 100))
            else:
                cv.setTrackbarPos(name, cls.window_name, value)
    
    @classmethod
    def get_parameters_from_gui(cls, param_type: Literal['hsv', 'threshold']) -> dict[str, int]:
        if param_type == 'threshold':
            return {
                "threshold": round(cv.getTrackbarPos("threshold", cls.window_name) / 100.00, 2)
            }        
        return {
            "hMin": cv.getTrackbarPos('hMin', cls.window_name),
            "sMin": cv.getTrackbarPos('sMin', cls.window_name),
            "vMin": cv.getTrackbarPos('vMin', cls.window_name),
            "hMax": cv.getTrackbarPos("hMax", cls.window_name),
            "sMax": cv.getTrackbarPos("sMax", cls.window_name),
            "vMax": cv.getTrackbarPos("vMax", cls.window_name),
            "sAdd": cv.getTrackbarPos("sAdd", cls.window_name),
            "sSub": cv.getTrackbarPos("sSub", cls.window_name),
            "vAdd": cv.getTrackbarPos("vAdd", cls.window_name),
            "vSub": cv.getTrackbarPos("vSub", cls.window_name),
        }
        
        