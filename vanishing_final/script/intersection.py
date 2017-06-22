#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

#line1 et line2 ne sont pas verticale
def getIntersection(line1, line2):

    x1=line1[0]
    y1=line1[1]
    x2=line1[2]
    y2=line1[3]
    x3=line2[0]
    y3=line2[1]
    x4=line2[2]
    y4=line2[3]
    a1=(y2-y1)/(x2-x1)
    b1=y1-a1*x1
    a2=(y4-y3)/(x4-x3)
    b2=y3-a2*x3
    x=(b1-b2)/(a2-a1)
    y=a1*x+b1
    
    return np.array([x,y])

#line1 ou lines est vertical
def getIntersectionV(line1, line2):

    x1=line1[0]
    y1=line1[1]
    x2=line1[2]
    y2=line1[3]
    x3=line2[0]
    y3=line2[1]
    x4=line2[2]
    y4=line2[3]
    
    a=(y4-y3)/(x4-x3)
    b=y3-a*x3
    y=a*x1+b
    
    return np.array([x1,y])
    
