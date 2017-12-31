# coding:utf-8

import cv2
import time
import numpy as np
from PIL import ImageGrab
from pykeyboard import PyKeyboard
长 = 945
高 = 551
pkd = PyKeyboard()
while cv2.waitKey(1) == -1:

    t = time.time()
    im = ImageGrab.grab((0, 0, 长, 高))
    im = np.asarray(im)

    # 226 222 216 213
    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img = np.where((img < 210) | (img > 240), img, 0)
    img = np.where(img == 0 , img, 255)

    closed = cv2.dilate(img, None, iterations=1)
    #closed = cv2.erode(closed, None, iterations=1)
    image, contours, hier = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(closed,contours,-1,128,3)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h

        if area <= -100:
            print(area)
            if x<长/2:
                pkd.tap_key('a')
            else:
                pkd.tap_key('d')
            if y<高/2:
                pkd.tap_key('w')
            else:
                pkd.tap_key('s')
            break
            #cv2.rectangle(closed, (x, y), (x + w, y + h), 128 , 2)
    print(time.time() - t)
    cv2.imshow("img", img)

    cv2.imshow("closed", closed)


cv2.destroyAllWindows()
