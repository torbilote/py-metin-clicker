import cv2 as cv
import numpy as np
from numpy.typing import NDArray
from cv2.typing import MatLike, Rect
from typing import Sequence, Optional
from app.constants import TEMPLATE_BASE

class Finder:
    templates: Optional[dict[str, any]] = None

    def __init__(self) -> None:
        ...

    @classmethod
    def add_template(cls, template_name: str, template_path : str) -> None:
        template_processed = cv.imread(template_path, cv.IMREAD_UNCHANGED)
        cls.templates[template_name] = {
            "template": template_processed,
            "width": template_processed.shape[1],
            "height": template_processed.shape[0],
            "threshold": None,
        }

    @classmethod
    def update_template_threshold(cls, template_name: str, threshold: float) -> None: 
        cls.templates[template_name][threshold] = threshold

    @classmethod
    def find_template_on_image(cls, template_name: str, base_image: NDArray | MatLike, threshold: float) -> Sequence[Rect]:

        result_of_finding = cv.matchTemplate(base_image, cls.templates[template_name]['template'], cv.TM_CCOEFF_NORMED)

        locations = np.where(result_of_finding >= threshold)
        locations = list(zip(*locations[::-1]))

        if not locations:
            return []

        rectangles = list()

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), cls.templates[template_name]['width'], cls.templates[template_name]['height']]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        max_results_per_image = 3

        if len(rectangles) > max_results_per_image:
            rectangles = rectangles[:max_results_per_image]

        return rectangles