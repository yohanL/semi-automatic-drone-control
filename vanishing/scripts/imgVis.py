#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def imgVis(img,p1,p2):


    width = float(np.size(img, 1))
 
    img=cv2.copyMakeBorder(img,0,0,int(width),0,cv2.BORDER_CONSTANT,value=(255,255,255))
    img=cv2.copyMakeBorder(img,0,0,0,int(width),cv2.BORDER_CONSTANT,value=(255,255,255))


    if(np.isnan(p2[0])):
       cv2.circle(img,(int(p1[0]+width),int(p1[1])),5,(125,255,0),-1)

    else:
       cv2.circle(img,(int(p1[0]+width),int(p1[1])),5,(125,255,0),-1)
       cv2.circle(img,(int(p2[0]+width),int(p2[1])),5,(125,255,0),-1)

    return img
