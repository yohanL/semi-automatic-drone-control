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

def erVP(image):

    start = time.time()

    img = cv2.imread(image,1)
    grey = cv2.imread(image,0)

    height = float(np.size(img, 0))
    width = float(np.size(img, 1))

    e=100 #epsilon 
    rayon=np.sqrt(height**2+width**2)/2 - e
  
    c1Points, drawn_img = findIntersection(image) #liste des points d'intersection repere cartesien 1 et l'image avec segments et pts d'intersection
    time2 = time.time()
    print("interPoint: "+str(time2 - start)) #time:0.147s
    pointsLen=len(c1Points)

    '''
    c2Points=[] #liste des points d'intersection repere cartesien 2 (milieu img)
    time3 = time.time()
    for l in range(0,pointsLen):
        c2Points.append(c2cP((width/2,height/2),c1Points[l]))
    print("timec2cp: "+ str(time.time()-time3))
   '''

    erPoints=[] #liste des points exterieurs
    #######################################################
    time3_1 = time.time()
    testPoint = np.asarray(c1Points)
    testPoint[:,0] = testPoint[:,0] - (width/2)
    testPoint[:,1] = testPoint[:,1] - (height/2)
    c2Points = testPoint.tolist()
    print("time c2cp array: "+str(time.time()-time3_1))
   # print( np.asarray(c2Points) is testPoint)
    #print(np.asarray(c2Points).shape)
    #print(testPoint.shape)
    
    
    time4 = time.time()
    for l in range(0,pointsLen):
        if(np.sqrt(c2Points[l][0]**2+c2Points[l][1]**2) >= rayon):
            erPoints.append(c2Points[l])
    print("time find erPoints CC: "+str(time.time()-time4))#time: 0.00938s
    
    erPointsLen=len(erPoints)

    time4_1 = time.time()
    
    print ('nb pts ER = '+str(erPointsLen))

    #pointInterER = np.asarray(erPoints)
    time5 = time.time()
    pointInterER = np.empty(shape=[0,2])
    for k in range(0, erPointsLen):
        pointInterER = np.insert(pointInterER,pointInterER.shape[0],c2pP(erPoints[k]),axis=0)
    print("time PointInterER PC: "+str(time.time()-time5) ) #time:0.0957s
    #print(pointInterER)


    #



    w = 0.04 #the width of bin of angle(angle coordinate)
   
    l = 30 #nb of bin in the sector we find 
    r = 1000   #sutibal radius for bound Pi of Pmax and Pmin

    m = int(2*math.pi/w)

    #pointCounter = np.empty(shape=[m])




    #count the number of point in each bin of angle and find the bin with most points
    '''
    time6 = time.time()
    j = 1
    counterERphi = []
    pointCopyPhi = pointInterER
    while j < m :
        i = 0
        c = 0
        while i < pointCopyPhi.shape[0] :
            if (((j-1)*w) <= pointCopyPhi[[i],[1]] < (j*w)):
                c+=1
                pointCopyPhi = np.delete(pointCopyPhi,i,axis=0)
            
                #pointCounter[j-1] = int(pointCounter[j-1])+1
                # print(pointCounter[j-1])
            else:
                i+=1
            
        counterERphi.append(c)
        j+=1
    
    #the last bin of angle [-math.pi+(m-1)*w,math.pi]

    i = 0
    c = 0
    while i < pointCopyPhi.shape[0]:
        if  (pointCopyPhi[[i],[1]] >=((m-1)*w) and pointCopyPhi[[i],[1]] < (2*math.pi)):
            c+=1
        i+=1
    counterERphi.append(c)
    print("time find counter angle: "+str(time.time()-time6))
    '''

    #####################################################
    time6_1 = time.time()
    pointERphi = pointInterER[:,1]
    counterPhi,bins = np.histogram(pointERphi,bins=157)
    counterERphi = counterPhi.tolist()
    print("time to find counter angle (histogram): "+str(time.time()-time6_1)) # time: 0.000186s


    
    ##print(counterERphi)

    #find the bin with the most point
    MaxPhi = max(counterERphi)
    #print(MaxPhi)

    indexPhi = counterERphi.index(MaxPhi)
    ##print(indexPhi)
    ##print(counterERphi[indexPhi])

    #count the number of point in the bin of r in the sector we have found  and find the bin with most points 

    #creat a array contain the points of the sector we find
    time7 = time.time()
    pointInterSector = np.empty(shape=[0,2])
    i = 0
    while i < pointInterER.shape[0]:
        if (pointInterER[[i],[1]] >= (indexPhi*w) and pointInterER[[i],[1]] < (indexPhi+1)*w):
            pointInterSector = np.insert(pointInterSector,pointInterSector.shape[0],pointInterER[i],axis=0)
        i+=1
    ##print(pointInterSector.shape)

    #find Pmax,Pmin,phiMax,phiMin
    Pmax = np.amax(np.amax(pointInterSector,1))
    Pmin = np.amin(np.amax(pointInterSector,1))
    ##print(Pmax)
    ##print(Pmin)
    phiMin = math.atan(Pmin/r)
    phiMax = math.atan(Pmax/r)
    #print(phiMin)
    #print(phiMax)

    #find the number of points in each bin
    #l = (phiMax - phiMin)//tau #number of bin for radius coordinate
    #print(l)
        
    j = 1
    p = [Pmin]  #the list of Pi
    counterERp = []
    pointCopyP = pointInterSector
    while j <= l:
        i = 0
        c = 0
        p.append(r*math.tan(phiMin + j*(phiMax-phiMin)/l))
        while i < pointCopyP.shape[0]:
            if (p[j-1] <= pointCopyP[i][0] < p[j]):
                c+=1
                pointCopyP = np.delete(pointCopyP,i,axis=0)
            else:
                i+=1  
        counterERp.append(c)
        j+=1
        
    #print("time find counter radius in the sector: "+str(time.time()-time7))
    
    ##print(p)
    ##print(counterERp)
    ##print(len(counterERp))  
    MaxP = max(counterERp)
    ##print(MaxP)
    indexP = counterERp.index(MaxP)
    ##print(indexP)

    ##find the candidate vanishing point

    i = 0
    vpER = np.empty(shape=[0,2])

    while i < pointInterSector.shape[0]:
        if p[indexP] < pointInterSector[i][0] < p[indexP+1]:
            vpER = np.insert(vpER,vpER.shape[0],pointInterSector[i],axis=0)
        i+=1

    
    print('nb de pts dans le secteur choisi = '+str(len(vpER))) 
    ##print(vpER)
    moy = np.mean(vpER, axis=0)


    print('VP coord polaires = '+str(moy))

    vpERc2 = p2cP(moy)

    vpERc1 = c2cP((-width/2,-height/2),vpERc2)

    print ('VP coord cart = '+str(vpERc1))

    print("time find counter radius in the sector: "+str(time.time()-time7))
#time:0.06618
    print ('temps exe = '+str(time.time()-start))
    
    imgVis(drawn_img,vpERc1,np.array([0,0]),c1Points)

    return vpERc1
