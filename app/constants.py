from abc import ABC
DEBUG_MODE = True

WINDOW_COORDINATES = {"top": 0, "left": 0, "width": 800, "height": 600}


class TEMPLATE_BASE(ABC):
    NAME            : str
    IMAGE_PATH      : str
    HSV_PARAMETERS  : dict[str, int]
    THRESHOLD       : float

class TEMPLATE_ARROW_BLUE(TEMPLATE_BASE):
    NAME            = "arrow_blue"
    IMAGE_PATH      = "templates/arrow_blue.jpg"
    HSV_PARAMETERS  = {'hMin': 0, 'sMin': 0, 'vMin': 0, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0}
    THRESHOLD       = 0.90
class TEMPLATE_ARROW_YELLOW(TEMPLATE_BASE):
    NAME            = "arrow_yellow"
    IMAGE_PATH      = "templates/arrow_yellow.jpg"
    HSV_PARAMETERS  = {'hMin': 0, 'sMin': 0, 'vMin': 0, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0}
    THRESHOLD       = 0.50

class TEMPLATE_ARROW_PURPLE(TEMPLATE_BASE):
    NAME            = "arrow_purple"
    IMAGE_PATH      = "templates/arrow_purple.jpg"
    HSV_PARAMETERS  = {'hMin': 0, 'sMin': 0, 'vMin': 0, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0}
    THRESHOLD       = 0.50

class TEMPLATE_FISHING_ROD(TEMPLATE_BASE):
    NAME            = "fishing_rod"
    IMAGE_PATH      = "templates/fishing_rod.jpg"
    HSV_PARAMETERS  = {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0}
    THRESHOLD       = 0.50
    
class TEMPLATE_ICON(TEMPLATE_BASE):
    NAME            = "icon"
    IMAGE_PATH      = "templates/icon.jpg"
    HSV_PARAMETERS  = {'hMin': 0, 'sMin': 0, 'vMin': 0, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0}
    THRESHOLD       = 0.60

class HOTKEYS:
    ACTION      = 'space'
    PICK_WORM   = '2'     

class TIMERS:
    PAUSE_WHEN_NEW_ROUND_STARTS         = 5.0
    PAUSE_AFTER_WORM_IS_PICKED          = 0.5
    WAITING_LIMIT_FOR_ICON_TO_APPEAR    = 10.0
    PAUSE_AFTER_ICON_APPEARS            = 2.5
    PAUSE_BEFORE_FISHING_ROD_APPEARS    = 1.0
    PAUSE_AFTER_FISHING_ROD_APPEARS     = 4.0
    WAITING_LIMIT_FOR_FISHING           = 10.0
    WAITING_LIMIT_FOR_ACTIVE_MODE       = 3.0
    INTERVAL_WHEN_FISHING_GREEN_MODE    = 0.0
    INTERVAL_WHEN_FISHING_BLUE_MODE     = 0.0
    INTERVAL_WHEN_FISHING_PURPLE_MODE   = 0.0
    INTERVAL_WHEN_FISHING_YELLOW_MODE   = 0.0

class COUNTERS:
    FINDINGS_LIMIT      = 3
    NO_FINDINGS_LIMIT   = 2

class STEPS:
    STEP_1  = '1' 
    STEP_2  = '2'
    STEP_3  = '3'
    STEP_4  = '4'
    STEP_5  = '5'
    STEP_6  = '6'
    STEP_7_BLUE  = '7_BLUE'
    STEP_7_YELLOW  = '7_YELLOW'
    STEP_7_PURPLE  = '7_PURPLE'
    STEP_8  = '8' 
    STEP_9  = '9'
    STEP_10 = '10'
    STEP_11 = '11'
    STEP_12 = '12'
    STEP_13 = '13'
    STEP_14 = '14'
    STEP_15 = '15'