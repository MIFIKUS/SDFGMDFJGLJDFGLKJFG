import cv2
import numpy as np


def matching(main_image_name, template_image_name, threshold=0.77) -> bool:
    """Сравнивает 2 изображения"""
    img_rgb = cv2.imread(main_image_name)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_image_name, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        i = pt
    try:
        return pt
    except:
        return False