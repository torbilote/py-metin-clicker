# pixels
WINDOW_COORDINATES : dict[str, int] = {"top": 0, "left": 150, "width": 450, "height": 400} 

HOTKEY_ACTION    : str = 'space'
HOTKEY_PICK_WORM : str = '2'

TEMPLATE_ARROW_BLUE_NAME           : str = "arrow_blue"
TEMPLATE_ARROW_BLUE_IMAGE_PATH     : str = "templates/arrow_blue.jpg"
# TEMPLATE_ARROW_BLUE_HSV_PARAMETERS : dict[str, int] = {'hMin': 85, 'sMin': 4, 'vMin': 0, 'hMax': 134, 'sMax': 217, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 43, 'vSub': 0}
TEMPLATE_ARROW_BLUE_HSV_PARAMETERS : dict[str, int] = {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0}
TEMPLATE_ARROW_BLUE_THRESHOLD      : float = 0.90 

TEMPLATE_ARROW_YELLOW_NAME           : str = "arrow_yellow"
TEMPLATE_ARROW_YELLOW_IMAGE_PATH     : str = "templates/arrow_yellow.jpg"
# TEMPLATE_ARROW_YELLOW_HSV_PARAMETERS : dict[str, int] = {'hMin': 0, 'sMin': 63, 'vMin': 58, 'hMax': 37, 'sMax': 255, 'vMax': 167, 'sAdd': 0, 'sSub': 18, 'vAdd': 38, 'vSub': 0}
TEMPLATE_ARROW_YELLOW_HSV_PARAMETERS : dict[str, int] = {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0}
TEMPLATE_ARROW_YELLOW_THRESHOLD      : float = 0.90

TEMPLATE_ARROW_PURPLE_NAME           : str = "arrow_purple"
TEMPLATE_ARROW_PURPLE_IMAGE_PATH     : str = "templates/arrow_purple.jpg"
# TEMPLATE_ARROW_PURPLE_HSV_PARAMETERS : dict[str, int] = {'hMin': 118, 'sMin': 55, 'vMin': 24, 'hMax': 179, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 22, 'vSub': 0}
TEMPLATE_ARROW_PURPLE_HSV_PARAMETERS : dict[str, int] = {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0}
TEMPLATE_ARROW_PURPLE_THRESHOLD      : float = 0.90

TEMPLATE_FISHING_ROD_NAME           : str = "fishing_rod"
TEMPLATE_FISHING_ROD_IMAGE_PATH     : str = "templates/fishing_rod.jpg"
TEMPLATE_FISHING_ROD_HSV_PARAMETERS : dict[str, int] = {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0}
TEMPLATE_FISHING_ROD_THRESHOLD      : float = 0.70

TEMPLATE_ICON_NAME           : str = "icon"
TEMPLATE_ICON_IMAGE_PATH     : str = "templates/icon.jpg"
TEMPLATE_ICON_HSV_PARAMETERS : dict[str, int] = {'hMin': 66, 'sMin': 58, 'vMin': 91, 'hMax': 120, 'sMax': 255, 'vMax': 255, 'sAdd': 0, 'sSub': 0, 'vAdd': 0, 'vSub': 0}
TEMPLATE_ICON_THRESHOLD      : float = 0.60

### -------------------------------------- ###
### --- place to configure your tester --- ###
### -------------------------------------- ###
TESTER_USE_MOCKED_SCREENSHOT  : bool = True # flag whether to use saved image instead of real screenshot.
TESTER_MOCKED_SCREENSHOT_PATH : str = 'mocks/test_arrow_yellow.jpg' # the path to saved image to use instead of real screenshot. Has effect only if the flag above is set to True.

TESTER_TEMPLATE_NAME = TEMPLATE_ARROW_PURPLE_NAME # the template you want to use for object detection
TESTER_TEMPLATE_HSV_PARAMETERS = TEMPLATE_ARROW_PURPLE_HSV_PARAMETERS # the hsv parameters you want to use for object detecion
TESTER_TEMPLATE_THRESHOLD = TEMPLATE_ARROW_PURPLE_THRESHOLD # the threshold you want to use for object detecion
### -------------------------------------- ###
### -------------------------------------- ###
### -------------------------------------- ###

# seconds
TIMER_PAUSE_WHEN_NEW_ROUND_STARTS       : float = 5.0 
TIMER_PAUSE_AFTER_WORM_IS_PICKED        : float = 0.5
TIMER_WAITING_LIMIT_FOR_ICON_TO_APPEAR  : float = 18.0
TIMER_PAUSE_AFTER_ICON_APPEARS          : float = 2.5
TIMER_PAUSE_BEFORE_FISHING_ROD_APPEARS  : float = 1.0
TIMER_PAUSE_AFTER_FISHING_ROD_APPEARS   : float = 4.0
TIMER_WAITING_LIMIT_FOR_FISHING         : float = 10.0
TIMER_WAITING_LIMIT_FOR_ACTIVE_MODE     : float = 3.0
TIMER_INTERVAL_WHEN_FISHING_GREEN_MODE  : float = 0.0
TIMER_INTERVAL_WHEN_FISHING_BLUE_MODE   : float = 0.0
TIMER_INTERVAL_WHEN_FISHING_PURPLE_MODE : float = 0.0
TIMER_INTERVAL_WHEN_FISHING_YELLOW_MODE : float = 0.0

STEP_1        : str = '1' 
STEP_2        : str = '2'
STEP_3        : str = '3'
STEP_4        : str = '4'
STEP_5        : str = '5'
STEP_6        : str = '6'
STEP_7_BLUE   : str = '7_BLUE'
STEP_7_YELLOW : str = '7_YELLOW'
STEP_7_PURPLE : str = '7_PURPLE'
STEP_8        : str = '8'



