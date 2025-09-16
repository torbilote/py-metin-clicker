import cv2 as cv

class GUI:
    window_name = "Trackbars"

    @classmethod
    def create_gui(cls) -> None:
        cv.namedWindow(cls.window_name, cv.WINDOW_NORMAL)
        cv.resizeWindow(cls.window_name, 800, 600)

        cv.createTrackbar('hMin', cls.window_name, 0, 179, lambda: None)
        cv.createTrackbar('sMin', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('vMin', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('hMax', cls.window_name, 0, 179, lambda: None)
        cv.createTrackbar('sMax', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('vMax', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('sAdd', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('sSub', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('vAdd', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('vSub', cls.window_name, 0, 255, lambda: None)
        cv.createTrackbar('treshold', cls.window_name, 0, 100, lambda: None)
    
    @classmethod
    def set_parameters_on_gui(cls, parameters: dict[str, int]) -> None:
        for name, value in parameters.items():
            cv.setTrackbarPos(name, cls.window_name, value)
    
    @classmethod
    def get_parameters_from_gui(cls) -> dict[str, int]:
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
            "treshold": cv.getTrackbarPos("treshold", cls.window_name),
        }
        
        
        
        