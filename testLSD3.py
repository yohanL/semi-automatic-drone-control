#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
from intersection import getIntersection

img = cv2.imread("couloir2.jpg",0)

lsd = cv2.createLineSegmentDetector(0)

lines = lsd.detect(img)[0]

#print (lines.dtype)

"""lines = np.array([
    [[0,0,400,400]],
    [[0,400,400,0]]
   ], dtype='float32')"""

"""lines = np.array([
    [[350,250,620,450]],
    [[0,400,150,250]]
   ], dtype='float32')"""

"""lines = np.array([
    [[  4.75734901e+01,   5.61679602e-01,   4.86730690e+01,   3.43978119e+01]],

    [[  5.58041878e+01,   2.06210423e+01,   5.53619576e+01,   6.03196263e-01]],

   ], dtype='float32')"""

"""print (lines[[0],[0]])
print (lines[[0],[0]].dtype)
print (lines[[0],[0]].shape)
print (lines.shape[0])"""

"""print np.array([
    lines[[0],[0],[1]]-lines[[0],[0],[3]],
    lines[[0],[0],[2]]-lines[[0],[0],[0]],
    lines[[0],[0],[0]]*lines[[0],[0],[3]]-lines[[0],[0],[2]]*lines[[0],[0],[1]]
    ])"""

###########



###########

n=lines.shape[0]

h = np.array([[0],[0],[1]])
v = np.array([[0],[1],[0]])

horizontal = []
vertical = []
i=0
z=0

while i<n:

    
    """l=np.array([
    lines[[i],[0],[1]]-lines[[i],[0],[3]],
    lines[[i],[0],[2]]-lines[[i],[0],[0]],
    lines[[i],[0],[0]]*lines[[i],[0],[3]]-lines[[i],[0],[2]]*lines[[i],[0],[1]]
    ])

    norm=np.linalg.norm(l)

    lh=np.dot(l.transpose(),h)/norm
    lv=np.dot(l.transpose(),v)/norm

    if lh>lv:
        vertical.append(l)
       # lines[[i],[0]]=np.array([[0,0,0,0]], dtype='float32')
    else:
        horizontal.append(l)
       # lines[[i],[0]]=np.array([[0,0,0,0]], dtype='float32')"""
    

    if np.absolute(lines[[i],[0],[0]]-lines[[i],[0],[2]])<20:
        lines[[i],[0]]=np.array([[0,0,0,0]], dtype='float32')
    if np.absolute(lines[[i],[0],[1]]-lines[[i],[0],[3]])<15:
        lines[[i],[0]]=np.array([[0,0,0,0]], dtype='float32')
        
    i+=1

i=0
j=0

lineslist = []

while i<n:

    if np.any(lines[[i],[0]] != 0.0):
        lineslist.append(lines[[i],[0]])
        j+=1
    i+=1

k=len(lineslist)
print(k)
pointslist=[]

for q in range(0,k-1):
   for p in range(q+1,k-1):
       pointslist.append(getIntersection(lineslist[q],lineslist[p]))
       cv.circle(img,getIntersection(lineslist[q],lineslist[p]),1,(0,0,255),-1)
print(len(pointslist))
print(pointslist)


#point=getIntersection(lines[0],lines[1])
#print(point)


drawn_img = lsd.drawSegments(img,lines)
drawn_img2 = 
cv2.imshow("LSD",drawn_img)
cv2.waitKey(0)
