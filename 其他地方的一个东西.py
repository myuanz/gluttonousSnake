#coding:utf-8
"""
Created on Fri Aug 11 08:36:01 2017

@author: prove
"""
from scipy import ndimage
from scipy.signal import convolve2d
import cv2
import time 
import numpy as np
from PIL import ImageGrab,Image
import ctypes as ct
def getselfname():
    pass

dd = ct.windll.LoadLibrary('ddx64.dll')
name=cv2.imread("name.png",0)

#camera = cv2.VideoCapture(0)
mog = cv2.createBackgroundSubtractorMOG2(history=1)
p=[0,0,0,0,0,0]
while cv2.waitKey(1)==-1:
    #s,im = camera.read()
    t=time.time()
    im=ImageGrab.grab((0,200,800,600))
    im=np.asarray(im)
    img=im.copy()
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    method = cv2.TM_CCOEFF_NORMED
    res = cv2.matchTemplate(img,name,method)
    loc = np.where(res >= 0.8)
    if any(loc[0]):
        y=loc[0][0]
        x=loc[1][0]
        p[0]=x
        p[1]=y
        w=23
        h=14
        cv2.rectangle(im, (x,y), (x+w, y+h), (255, 255, 0), 1)


        

    fgmask=mog.apply(img)
    img=fgmask.copy()
    blu = cv2.blur(img, (9, 9))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))

    closed = cv2.morphologyEx(blu, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=16)

    (_, closed) = cv2.threshold(closed, 90, 255, cv2.THRESH_BINARY)


    
    image, contours, hier = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # find bounding box coordinates
        x,y,w,h = cv2.boundingRect(c)
        area=w*h
        #if area>=5000:print (area,1.0*h/w)
        if ((area <=25000 and area>=8000 and 1.0*h/w>=0.7 and 1.0*h/w<=2)) :
            

            if p[0]>=x and p[0]<=x+w and p[1]+200>=y and p[1]<=y+h:
                print ("character in ",x,y)
            else:
                p[2]=x
                p[3]=y
                p[4]=w
                p[5]=h
                print ("enemy in ",x,y)
                dd.DD_mov(x,y+200)
            cv2.rectangle(im, (x,y), (x+w, y+h), (255, 255, 0), 2)
    print (time.time()-t)
    cv2.imshow("new", im)
    cv2.imshow("closed", closed)

#camera.release()




cv2.destroyAllWindows()
