from app.windowcapturer import WindowCapturer
from app.hsvfilter import HsvFilter
from app.finder import Finder
from app.bot import Bot


DEBUG_MODE = True
WINDOW_NAME = 'Mt2009'
HSV_PARAMETERS = {
    "hMin": 0, 
    "sMin": 0, 
    "vMin": 63, 
    "hMax": 179, 
    "sMax": 200, 
    "vMax": 255, 
    "sAdd": 0, 
    "sSub": 0, 
    "vAdd": 0, 
    "vSub": 12, 
}
TEMPLATES_TO_DETECT = {
    "arrow_blue": "img/arrow_blue.jpg",
    "arrow_purple": "img/arrow_purple.jpg",
    "arrow_yellow": "img/arrow_yellow.jpg",
    "fishing_rod": "img/fishing_rod.jpg",
    "icon": "img/icon.jpg",
}

if __name__ == "__main__":
    window_capturer = WindowCapturer(WINDOW_NAME)
    hsv_filter = HsvFilter(HSV_PARAMETERS)
    finder = Finder(TEMPLATES_TO_DETECT)
    bot = Bot(window_capturer, finder, hsv_filter, DEBUG_MODE)

    bot.run()