from app.screenshot import WindowCapturer
from app.hsvfilter import HsvFilter
from app.find import Finder
from app import run
import cv2 as cv
from loguru import logger


TEMPLATES_TO_USE = "arrow_yellow"
HSV_PARAMETERS_TO_USE = run.HSV_PARAMETERS["arrow_yellow"]
THRESHOLDS_TO_USE = run.THRESHOLDS["arrow_yellow"]

if __name__ == "__main__":
    window_capturer = WindowCapturer(run.WINDOW_COORDINATES)
    hsv_filter = HsvFilter(HSV_PARAMETERS_TO_USE, gui=True)
    finder = Finder(run.TEMPLATES)
    run = run.Bot(window_capturer, finder, hsv_filter, run.DEBUG_MODE)


    while True:
        hsv_parameters_from_controls = run.hsv_filter.get_hsv_filter_from_controls()
        results = run.find(
            TEMPLATES_TO_USE,
            THRESHOLDS_TO_USE,
            hsv_parameters_from_controls,
            mocked_image_path="mocked_screenshots/test_arrow_purple.jpg",
        )
        
        logger.debug(f'Results: {results}')

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

    logger.debug(f'Latest HSV Filter Configuration:\n {run.hsv_filter.hsv_parameters}')
