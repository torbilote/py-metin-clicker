from app import constants as c
from app.utils import add_template, make_screenshot, apply_filter_on_image, find_template_on_image, draw_rectangles, create_gui, set_parameters_on_gui, get_parameters_from_gui, load_image
import cv2 as cv


def main() -> None:
    add_template(c.TEMPLATE_ARROW_BLUE_NAME, c.TEMPLATE_ARROW_BLUE_IMAGE_PATH)
    add_template(c.TEMPLATE_ARROW_PURPLE_NAME, c.TEMPLATE_ARROW_PURPLE_IMAGE_PATH)
    add_template(c.TEMPLATE_ARROW_YELLOW_NAME, c.TEMPLATE_ARROW_YELLOW_IMAGE_PATH)
    add_template(c.TEMPLATE_FISHING_ROD_NAME, c.TEMPLATE_FISHING_ROD_IMAGE_PATH)
    add_template(c.TEMPLATE_ICON_NAME, c.TEMPLATE_ICON_IMAGE_PATH)
    
    ### --- place to configure --- ###
    template_name = c.TEMPLATE_FISHING_ROD_NAME 
    template_hsv_parameters = c.TEMPLATE_FISHING_ROD_HSV_PARAMETERS
    template_threshold =  c.TEMPLATE_FISHING_ROD_THRESHOLD
    
    use_mocked_screenshot = False
    mocked_screenshot_path = '<path_to_your_screenshot>' 
    ### -------------------------- ###

    create_gui()
    set_parameters_on_gui({**template_hsv_parameters, "threshold": template_threshold})

    while True:
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
        
        if use_mocked_screenshot:
            screenshot_raw = load_image(mocked_screenshot_path)
        else:
            screenshot_raw = make_screenshot(c.WINDOW_COORDINATES)

        fresh_hsv_parameters = get_parameters_from_gui('hsv')
        fresh_threshold = get_parameters_from_gui('threshold')
        screenshot_hsv = apply_filter_on_image(screenshot_raw, fresh_hsv_parameters)
        findings = find_template_on_image(template_name, screenshot_hsv, **fresh_threshold)
        draw_rectangles(screenshot_hsv, findings)


if __name__ == "__main__":
    main()