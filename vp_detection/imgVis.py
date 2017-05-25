#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def imgVis(img,p1,p2,p):
    width = float(np.size(img, 1))
    height = float(np.size(img, 0))

    xmax=np.maximum(p1[0],p2[0])
    ymax=np.maximum(p1[1],p2[1])

    xmin=np.minimum(p1[0],p2[0])
    ymin=np.minimum(p1[1],p2[1])

    if (xmin<0):
        img=cv2.copyMakeBorder(img,0,0,int(-xmin+20),0,cv2.BORDER_CONSTANT,value=(255,255,255))
    if (xmax>width):
        img=cv2.copyMakeBorder(img,0,0,0,int(xmax-width+20),cv2.BORDER_CONSTANT,value=(255,255,255))
    if (ymin<0):
        img=cv2.copyMakeBorder(img,int(-ymin+20),0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
    if (ymax>height):
        img=cv2.copyMakeBorder(img,0,int(ymax-height+20),0,0,cv2.BORDER_CONSTANT,value=(255,255,255))

    for m in range(0,len(p)):
        cv2.circle(img,(int(p[m][0]),int(p[m][1])),2,(0,0,0),-1)
        
    cv2.circle(img,(int(p1[0]),int(p1[1])),5,(125,255,0),-1)
    cv2.circle(img,(int(p2[0]),int(p2[1])),5,(125,255,0),-1)

    #cv2.imwrite('img6vp.png',img)
    cv2.imshow("VP",img)
    cv2.waitKey(0)
