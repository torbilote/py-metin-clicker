import numpy as np
import win32gui, win32ui, win32con
from typing import Optional
from numpy.typing import NDArray


class WindowCapturer:

    def __init__(self, window_name: Optional[str] = None) -> None:

        self.window_width: int = 0 # in pixels
        self.window_height: int = 0 # in pixels
        self.hwnd: any = None
        self.window_offset_from_left: int = 0 # the distance from the left to be ignored from the relevant window
        self.window_offset_from_top: int = 0
        self.full_offset_from_left: int = 0 # the distance from the left of the full screen up to the of the window + the distance of window offset from left
        self.full_offset_from_top: int = 0

        border_pixels = 8 # left, right, bottom
        titlebar_pixels = 30 # top

        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if not window_name:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_sides = win32gui.GetWindowRect(self.hwnd)
        self.window_width = window_sides[2] - window_sides[0]
        self.window_height = window_sides[3] - window_sides[1]

        # account for the window border and titlebar and cut them off
        self.window_width = self.window_width - (border_pixels * 2)
        self.window_height = self.window_height - titlebar_pixels - border_pixels

        self.window_offset_from_left = border_pixels
        self.window_offset_from_top = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.full_offset_from_left = window_sides[0] + self.window_offset_from_left
        self.full_offset_from_top = window_sides[1] + self.window_offset_from_top

    def get_screenshot(self) -> NDArray:

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.window_width, self.window_height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.window_width, self.window_height), dcObj, (self.window_offset_from_left, self.window_offset_from_top), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img: NDArray = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.window_height, self.window_width, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        screenshot = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        return np.ascontiguousarray(screenshot)

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def _winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                window_name = win32gui.GetWindowText(hwnd)
                if window_name:
                    print(window_name)
        win32gui.EnumWindows(_winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_pixel_position_in_window(self, pixel_position_from_left: int, pixel_position_from_top: int) -> tuple[int, int]:
        return (pixel_position_from_left + self.full_offset_from_left, pixel_position_from_top + self.full_offset_from_top)