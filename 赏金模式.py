# coding:utf-8


import cv2
import time
import numpy as np
from PIL import ImageGrab
from pykeyboard import PyKeyboard

长 = 945
高 = 551
pkd = PyKeyboard()

viedo = cv2.VideoCapture('test.mp4')

ret = True
ret, im = viedo.read()


font=cv2.FONT_HERSHEY_SIMPLEX#使用默认字体

img=cv2.putText(im,'3',(0,40),font,1.2,(255,255,255),2)#添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细

while (cv2.waitKey(1) == -1) and (ret == True):

    t = time.time()
    # im = ImageGrab.grab((0, 0, 长, 高))
    # im = np.asarray(im)


    img = im

    closed = img.copy()
    closed = cv2.cvtColor(closed, cv2.COLOR_BGR2GRAY)
    closed = np.where((closed > 60), closed, 0)
    closed = np.where(closed == 0, closed, 255)

    closed = cv2.dilate(closed, None, iterations=1)
    # closed = cv2.erode(closed, None, iterations=1)
    image, contours, hier = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #先腐蚀找吃的,然后膨胀确定蛇

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        if area >= 100000000:
            cv2.drawContours(img, c, -1, (255,255,0), 3)
            img = cv2.putText(img, str(area), (x, y), font, 1, (255, 255, 0), 2)
        if 200000 >= area >= 10000: 
            cv2.drawContours(img, c, -1, (255, 255, 0), 3)
            img = cv2.putText(img, str("a snake"), (x, y), font, 1, (255, 255, 0), 2)
        if 1000 >= area >= 100:
            cv2.drawContours(img, c, -1, (0, 255, 255), 3)
            img = cv2.putText(img, str("little food"), (x, y), font, 1, (0, 255, 255), 2)
        if 2000 >= area >= 1000:
            cv2.drawContours(img, c, -1, (255, 0, 255), 3)
            img = cv2.putText(img, str("big food"), (x, y), font, 1, (255, 0, 255), 2)

        if area <= -100:
            print(area)
            if x < 长 / 2:
                pkd.tap_key('a')
            else:
                pkd.tap_key('d')
            if y < 高 / 2:
                pkd.tap_key('w')
            else:
                pkd.tap_key('s')
            break
            # cv2.rectangle(closed, (x, y), (x + w, y + h), 128 , 2)
    #print(time.time() - t)
    cv2.imshow("img", img)
    cv2.imshow("closed", closed)
    ret, im = viedo.read()
    time.sleep(1/30)
cv2.destroyAllWindows()
