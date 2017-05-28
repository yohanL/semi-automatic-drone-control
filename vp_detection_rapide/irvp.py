
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from intersection import *
from conversion import *
from imgVis import *
from findInter import *
import math
import time

def irVP(image):

    start = time.time()

    img = cv2.imread(image,1)
    grey = cv2.imread(image,0)

    nbInter = 30 #nombre d'intervalles en x
    
    height = float(np.size(img, 0))
    width = float(np.size(img, 1))
    
    e=0 #epsilon 
    r=float(np.sqrt(height**2+width**2)/2 + e)

    c1Points, drawn_img = findIntersection(image) #liste des points d'intersection repere cartesien 1 et l'image avec segments et points d'intersection

    pointsLen=len(c1Points)

    time1 = time.time()
    '''
    c2Points=[] #liste des points d'intersection repere cartesien 2 (milieu img)
    
    for l in range(0,pointsLen):
        c2Points.append(c2cP((width/2,height/2),c1Points[l]))

    print("time c2cP: "+str(time.time()-time1))
    '''
    ##################################################
    testPoint = np.asarray(c1Points)
    testPoint[:,0] = testPoint[:,0] - (width/2)
    testPoint[:,1] = testPoint[:,1] - (height/2)
    c2Points = testPoint.tolist()
    print("time c2cP: "+str(time.time()-time1))

    
    irPoints=[] #liste des points interieurs
    
    for l in range(0,pointsLen):
        if(np.sqrt(c2Points[l][0]**2+c2Points[l][1]**2) < r):
            irPoints.append(c2Points[l])

    irPointsLen = len(irPoints)
    print('nb pts IR = '+str(irPointsLen))

    time2 = time.time()
    xList=[]
   # r = (2*r//nbInter + 1)*nbInter/2
    for l in range(0,nbInter):
        new_list = []
        for m in range(0,irPointsLen):
            if (irPoints[m][0]>=-r+2*r*l/(nbInter) and irPoints[m][0]<-r+2*r*(l+1)/(nbInter)):
                new_list.append(irPoints[m])
        xList.append(new_list)
    
    print("time find x bin: "+str(time.time()-time2))
    Hx=[]

    time3 = time.time()
    for l in range(0,len(xList)):
        y=[]
        for k in range(0,len(xList[l])):
            y.append(xList[l][k][1])
        if (len(y)>4): #si au moins 5 points dans l'intervalle
            Hx.append(len(xList[l])/np.var(y))
        else:
            Hx.append(0)
    print("time find Hx : "+str(time.time()-time3))
    iMax=Hx.index(max(Hx)) #indice max Hx

    maxLen=len(xList[iMax])

    print('nb de pts dans l''invervalle choisi = '+str(maxLen))
    
    mx=0
    my=0
    for k in range(0, maxLen):
        mx=mx+xList[iMax][k][0]/maxLen
    for k in range(0, maxLen):
        my=my+xList[iMax][k][1]/maxLen

    irVP=c2cP((-width/2,-height/2),np.array([mx,my]))
    print('coordonnees VP = '+str(irVP))

    print ('temps exe = '+str(time.time()-start))

    imgVis(drawn_img,irVP,np.array([0,0]),c1Points)

    return irVP
