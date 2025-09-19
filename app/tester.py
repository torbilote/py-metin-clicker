from app import constants as c
from app.utils import add_template, make_screenshot, apply_filter_on_image, find_template_on_image, draw_and_show_rectangles, draw_and_save_rectangles, create_gui, set_parameters_on_gui, get_parameters_from_gui, load_image, save_screenshot
import cv2 as cv


def main() -> None:
    add_template(c.TEMPLATE_ARROW_BLUE_NAME, c.TEMPLATE_ARROW_BLUE_IMAGE_PATH)
    add_template(c.TEMPLATE_ARROW_PURPLE_NAME, c.TEMPLATE_ARROW_PURPLE_IMAGE_PATH)
    add_template(c.TEMPLATE_ARROW_YELLOW_NAME, c.TEMPLATE_ARROW_YELLOW_IMAGE_PATH)
    add_template(c.TEMPLATE_FISHING_ROD_NAME, c.TEMPLATE_FISHING_ROD_IMAGE_PATH)
    add_template(c.TEMPLATE_ICON_NAME, c.TEMPLATE_ICON_IMAGE_PATH)
        
    create_gui()
    set_parameters_on_gui({**c.TESTER_TEMPLATE_HSV_PARAMETERS, "threshold": c.TESTER_TEMPLATE_THRESHOLD})

    while True:
        if c.TESTER_USE_MOCKED_SCREENSHOT:
            screenshot_raw = load_image(c.TESTER_MOCKED_SCREENSHOT_PATH)
        else:
            screenshot_raw = make_screenshot(c.WINDOW_COORDINATES)

        fresh_hsv_parameters = get_parameters_from_gui('hsv')
        fresh_threshold = get_parameters_from_gui('threshold')
        screenshot_hsv = apply_filter_on_image(screenshot_raw, fresh_hsv_parameters)
        findings = find_template_on_image(c.TESTER_TEMPLATE_NAME, screenshot_hsv, **fresh_threshold)
        draw_and_show_rectangles(screenshot_hsv, findings)
        draw_and_save_rectangles(screenshot_hsv, findings, f'bot_screenshots/{c.TESTER_TEMPLATE_NAME}.jpg')

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            print(f"Last params: {fresh_hsv_parameters}\n{fresh_threshold}\n")
            break

if __name__ == "__main__":
    main()