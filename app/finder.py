import cv2 as cv
import numpy as np
from numpy.typing import NDArray
from cv2.typing import MatLike
from typing import Optional

class Finder:
    # constructor
    def __init__(self, images_paths: list[str], base_image: Optional[NDArray|MatLike] = None, method: int = cv.TM_CCOEFF_NORMED) -> None:
        self.base_image = base_image

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method
        self.images = list()
        for image_path in images_paths:
            # load the image we're trying to match
            # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
            image = cv.imread(image_path, cv.IMREAD_UNCHANGED)

            # Save the dimensions of the image       
            self.images.append({
                "image": image,
                "width": image.shape[1],
                "height": image.shape[0],
                "path": image_path,
            })
    
    def find(self, threshold: float = 0.5, max_results_per_image: int = 10) -> list[dict[str,Optional[tuple]]]:
        result = list()
        for image in self.images:
            # run the OpenCV algorithm
            result_of_finding = cv.matchTemplate(self.base_image, image['image'], self.method)

            # Get the all the positions from the match result that exceed our threshold
            locations = np.where(result_of_finding >= threshold)
            locations = list(zip(*locations[::-1]))
            # print(locations)

            # if we found no results, return now. this reshape of the empty array allows us to 
            # concatenate together results without causing an error
            if not locations:
                return np.array([], dtype=np.int32).reshape(0, 4)

            # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
            # locations by using groupRectangles().
            # First we need to create the list of [x, y, w, h] rectangles
            rectangles = []
            for loc in locations:
                rect = [int(loc[0]), int(loc[1]), image['width'], image['height']]
                # Add every box to the list twice in order to retain single (non-overlapping) boxes
                rectangles.append(rect)
                rectangles.append(rect)

            # Apply group rectangles.
            # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
            # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
            # in the result. I've set eps to 0.5, which is:
            # "Relative difference between sides of the rectangles to merge them into a group."
            rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
            #print(rectangles)

            # for performance reasons, return a limited number of results.
            # these aren't necessarily the best results.
            if len(rectangles) > max_results_per_image:
                print('Warning: too many results, raise the threshold.')
                rectangles = rectangles[:max_results_per_image]

            result.append({ image['path']: rectangles })

        return result


