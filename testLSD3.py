#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

img = cv2.imread("couloir2.jpg",0)

lsd = cv2.createLineSegmentDetector(0)

lines = lsd.detect(img)[0]

#print (lines.dtype)

lines = np.array([
    [[350,250,620,450]],
    [[0,400,150,250]]
   ], dtype='float32')

"""lines = np.array([
    [[  4.75734901e+01,   5.61679602e-01,   4.86730690e+01,   3.43978119e+01]],

    [[  5.58041878e+01,   2.06210423e+01,   5.53619576e+01,   6.03196263e-01]],

   ], dtype='float32')"""


#print (lines)



drawn_img = lsd.drawSegments(img,lines)

cv2.imshow("LSD",drawn_img)
cv2.waitKey(0)
