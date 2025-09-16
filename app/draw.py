import cv2 as cv
from numpy.typing import NDArray
from cv2.typing import MatLike, Rect
from typing import Sequence


class Draw:
    line_color = (0, 255, 0) # BGR
    line_type = cv.LINE_4

    @classmethod
    def draw_rectangles(cls, base_image: NDArray|MatLike, rectangles: Sequence[Rect]) -> NDArray|MatLike:

        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(base_image, top_left, bottom_right, cls.line_color, lineType=cls.line_type)
            
        cv.imshow('Screenshot', base_image)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
        
        return base_image