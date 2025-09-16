import cv2 as cv
import numpy as np
from numpy.typing import NDArray
from cv2.typing import MatLike, Rect
from typing import Sequence

class Find:
    # constructor
    def __init__(self, templates: dict[str, str]) -> None:
        self.templates = dict()

        for template_name, template_path in templates.items():
            template = cv.imread(template_path, cv.IMREAD_UNCHANGED)
    
            self.templates[template_name] = {
                "template": template,
                "width": template.shape[1],
                "height": template.shape[0],
            }
    
    def find_template_on_image(self, template_name: str, base_image: NDArray|MatLike, threshold: float = 0.5, max_results_per_image: int = 3) -> Sequence[Rect]:
        result_of_finding = cv.matchTemplate(base_image, self.templates[template_name]['template'], cv.TM_CCOEFF_NORMED)

        locations = np.where(result_of_finding >= threshold)
        locations = list(zip(*locations[::-1]))

        if not locations:
            return []

        rectangles = list()

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.templates[template_name]['width'], self.templates[template_name]['height']]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        if len(rectangles) > max_results_per_image:
            rectangles = rectangles[:max_results_per_image]

        return rectangles