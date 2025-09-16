import cv2 as cv
from numpy.typing import NDArray
from cv2.typing import MatLike, Rect
from typing import Sequence


class Drawer:
    def __init__(self) -> None:
        ...

    # given a list of [x, y, w, h] rectangles and a canvas image to draw on, return an image with
    # all of those rectangles drawn
    @staticmethod
    def draw_rectangles(base_image: NDArray|MatLike, rectangles: Sequence[Rect]) -> NDArray|MatLike:
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(base_image, top_left, bottom_right, line_color, lineType=line_type)
            
        cv.imshow('Screenshot', base_image)
        
        return base_image