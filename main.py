# coding:utf-8

import cv2
import time
import numpy as np
from PIL import ImageGrab

mog = cv2.createBackgroundSubtractorMOG2(history=1)

while cv2.waitKey(1) == -1:
    # s,im = camera.read()
    t = time.time()
    im = ImageGrab.grab((0, 0, 304, 220))
    im = np.asarray(im)

    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations=3)


    (_, closed) = cv2.threshold(closed, 150, 255, cv2.THRESH_BINARY)
    closed = cv2.dilate(closed, None, iterations=1)
    image, contours, hier = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), 2)
    print(time.time() - t)
    cv2.imshow("new", im)
    cv2.imshow("closed", closed)

# camera.release()


cv2.destroyAllWindows()
