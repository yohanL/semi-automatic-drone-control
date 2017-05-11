#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

def getIntersection(line1, line2):
    s1 = np.array([line1[[0],[0]],line1[[0],[1]]])
    e1 = np.array([line1[[0],[2]],line1[[0],[3]]])

    s2 = np.array([line2[[0],[0]],line2[[0],[1]]])
    e2 = np.array([line2[[0],[2]],line2[[0],[3]]])

    a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
    b1 = s1[1] - (a1 * s1[0])

    a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
    b2 = s2[1] - (a2 * s2[0])

    #if abs(a1 - a2) < sys.float_info.epsilon:
        #return False

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1

    x1 = float(x)
    y1 = float(y)
    
    return np.array([x1,y1])


    
