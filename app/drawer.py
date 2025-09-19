import cv2 as cv
from numpy.typing import NDArray
from cv2.typing import MatLike, Rect
from typing import Sequence
from uuid import uuid4

class Drawer:
    line_color: tuple = (0, 255, 0) # BGR
    line_type: int = cv.LINE_4

    
    @classmethod
    def draw_and_show_rectangles(cls, base_image: NDArray | MatLike, coordinates: Sequence[Rect]) -> None:
        for (x, y, w, h) in coordinates:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(base_image, top_left, bottom_right, cls.line_color, lineType=cls.line_type)
            
        cv.imshow('Screenshot', base_image)

    @classmethod
    def draw_and_save_rectangles(cls, base_image: NDArray | MatLike, coordinates: Sequence[Rect], file_path: str) -> None:
        for (x, y, w, h) in coordinates:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(base_image, top_left, bottom_right, cls.line_color, lineType=cls.line_type)
        
        if len(coordinates) > 0:
            file_path = file_path.replace('.jpg', f'_{str(uuid4())}.jpg')
            cv.imwrite(file_path, base_image)
            print(f'writing to {file_path}')
