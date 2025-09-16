import enum

DEBUG_MODE = True
WINDOW_COORDINATES = {"top": 0, "left": 0, "width": 800, "height": 600}

class HOTKEYS(enum.Enum):
    SPACE       = 'space'
    DIGIT_TWO   = '2' 

class TEMPLATES(enum.Enum):
    ARROW_BLUE: dict = {
        "image_path": "templates/arrow_blue2.jpg",
        "hsv_parameters": {'hMin': 84, 'sMin': 20, 'vMin': 54, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0},
        "threshold": 0.90,
    }
    ARROW_YELLOW: dict = {
        "image_path": "templates/arrow_yellow2.jpg",
        "hsv_parameters": {'hMin': 0, 'sMin': 0, 'vMin': 79, 'hMax': 36, 'sMax': 114, 'vMax': 255, 'sAdd': 45, 'sSub': 0, 'vAdd': 0, 'vSub': 0},
        "threshold": 0.50,
    }
    FISHING_ROD: dict = {
        "image_path": "templates/fishing_rod.jpg",
        "hsv_parameters": {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0},
        "threshold": 0.50,
    }
    ICON: dict = {
        "image_path": "templates/icon2.jpg",
        "hsv_parameters": {'hMin': 0, 'sMin': 0, 'vMin': 143, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 190, 'vAdd': 0, 'vSub': 0},
        "threshold": 0.60,
    }
    
class TIMERS(enum.IntEnum):
    PAUSE_WHEN_NEW_ROUND_STARTS         : 5.00 
    PAUSE_WHEN_ICON_APPEARS             : 2.50
    PAUSE_BEFORE_FISHING_ROD_APPEARS    : 1.00
    PAUSE_BEFORE_FISHING_STARTS         : 4.00
    INTERVAL_WHEN_FISHING_GREEN_MODE    : 0.00
    INTERVAL_WHEN_FISHING_BLUE_MODE     : 0.00
    INTERVAL_WHEN_FISHING_PURPLE_MODE   : 0.00
    INTERVAL_WHEN_FISHING_YELLOW_MODE   : 0.00

class COUNTERS(enum.IntEnum):
    FINDINGS_LIMIT      = 3
    NO_FINDINGS_LIMIT   = 2

class STEPS(enum.IntEnum):
    STEP_1  = enum.auto() 
    STEP_2  = enum.auto()
    STEP_3  = enum.auto()
    STEP_4  = enum.auto()
    STEP_5  = enum.auto()
    STEP_6  = enum.auto()
    STEP_7  = enum.auto()
    STEP_8  = enum.auto() 
    STEP_9  = enum.auto()
    STEP_10 = enum.auto()
    STEP_11 = enum.auto()
    STEP_12 = enum.auto()
    STEP_13 = enum.auto()
    STEP_14 = enum.auto()
    STEP_15 = enum.auto()