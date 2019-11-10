import os
import glob
import cv2
import numpy as np


def extract_darkness_image(path):

    img = cv2.imread(path)
    # cv2.imshow("origin image", img)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _, _, img_v = cv2.split(img_hsv)
    # cv2.imshow("lighting image", img_v)

    norm_v = cv2.normalize(img_v, None, 0, 255, cv2.NORM_MINMAX)
    # cv2.imshow("normalize image", norm_v)

    kernel = np.ones((5, 5), np.uint8)
    dilate_v = cv2.dilate(norm_v, kernel, iterations=2)
    # cv2.imshow("dilate_v", dilate_v)

    erode_v = cv2.erode(dilate_v, kernel, iterations=2)
    # cv2.imshow("erode_v", erode_v)

    equ_v = cv2.equalizeHist(erode_v)
    # cv2.imshow("equ", equ_v)

    ret, thresh_v = cv2.threshold(equ_v, 10, 255, cv2.THRESH_BINARY)
    thresh_v_not = cv2.bitwise_not(thresh_v)
    # cv2.imshow("th1", thresh_v)
    # cv2.waitKey(0)

    return img, thresh_v_not


class ExtractDarkness:

    def __init__(self, dir_path, debug=False):

        self.debug = debug

        self.img_paths = glob.glob(os.path.join(dir_path, "bg", "*.png"))

    def extract_darkness(self):

        for img_path in self.img_paths:

            filename = os.path.basename(img_path)
            origin_img, dark_img = extract_darkness_image(img_path)
            cv2.imshow("dark part", dark_img)
            contours, _ = cv2.findContours(dark_img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
            boundingRect = cv2.boundingRect(sorted_contours[0])
            cv2.rectangle(origin_img, (boundingRect[0], boundingRect[1]),
                          (boundingRect[0] + boundingRect[2], boundingRect[1] + boundingRect[3]), (0, 0, 255), 3)

            cv2.imshow("extracted image{}".format(filename), origin_img)
            cv2.waitKey()
