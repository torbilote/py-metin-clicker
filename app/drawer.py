import cv2 as cv
from numpy.typing import NDArray
from cv2.typing import MatLike, Rect
from typing import Sequence
from uuid import uuid4
import random

class Drawer:
    line_color: tuple = (0, 255, 0) # BGR
    line_type: int = cv.LINE_4

    
    @classmethod
    def show_rectangles(cls, base_image: NDArray | MatLike, coordinates: Sequence[Rect]) -> None:
        for (x, y, w, h) in coordinates:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(base_image, top_left, bottom_right, cls.line_color, lineType=cls.line_type)
            
        cv.imshow('Screenshot', base_image)

    @classmethod
    def save_rectangles(cls, base_image: NDArray | MatLike, coordinates: Sequence[Rect], file_prefix: str) -> None:
        to_save: bool = random.choice(range(100)) < 20 # save 20% of made screenshots

        path = f'bot_screenshots/{file_prefix}_{str(uuid4())}.jpg'

        for (x, y, w, h) in coordinates:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(base_image, top_left, bottom_right, cls.line_color, lineType=cls.line_type)
        
        if len(coordinates) > 0 and to_save:
            cv.imwrite(path, base_image)

