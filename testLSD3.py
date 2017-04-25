#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

img = cv2.imread("couloir2.jpg",0)

lsd = cv2.createLineSegmentDetector(0)

lines = lsd.detect(img)[0]
"""lines = np.array([
    [[0, 0, 100, 100]]
   ] )"""

print lines

#img2 = cv2.imread("black.png",0)

drawn_img = lsd.drawSegments(img,lines)

cv2.imshow("LSD",drawn_img)
#cv2.imshow("lines",img)
cv2.waitKey(0)
