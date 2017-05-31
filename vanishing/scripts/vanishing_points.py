#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from intersection import *
from conversion import *
from findInter import *
import math
import time

def vp(image):

    start = time.time()

    img = image

    nbInter = 30 #nombre d'intervalles en x
    
    height = float(np.size(img, 0))
    width = float(np.size(img, 1))
    
    e1=0 #epsilon
    e2=100
    rayon1=float(np.sqrt(height**2+width**2)/2 + e1)
    rayon2=float(np.sqrt(height**2+width**2)/2 - e2)

    c1Points, drawn_img = findIntersection(image) #liste des points d'intersection repere cartesien 1 et l'image avec segments et points d'intersection

    pointsLen=len(c1Points)

    time1 = time.time()
  
    ##################################################
    testPoint = np.asarray(c1Points)
    testPoint[:,0] = testPoint[:,0] - (width/2)
    testPoint[:,1] = testPoint[:,1] - (height/2)
    c2Points = testPoint.tolist()
    #print("time c2cP: "+str(time.time()-time1))

    
    irPoints=[] #liste des points interieurs
    
    for l in range(0,pointsLen):
        if(np.sqrt(c2Points[l][0]**2+c2Points[l][1]**2) < rayon1):
            irPoints.append(c2Points[l])

    irPointsLen = len(irPoints)
    #print('nb pts IR = '+str(irPointsLen))

    time2 = time.time()
    xList=[]
   # r = (2*r//nbInter + 1)*nbInter/2
    for l in range(0,nbInter):
        new_list = []
        for m in range(0,irPointsLen):
            if (irPoints[m][0]>=-rayon1+2*rayon1*l/(nbInter) and irPoints[m][0]<-rayon1+2*rayon1*(l+1)/(nbInter)):
                new_list.append(irPoints[m])
        xList.append(new_list)
    
    #print("time find x bin: "+str(time.time()-time2))
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
    #print("time find Hx : "+str(time.time()-time3))
    iMax=Hx.index(max(Hx)) #indice max Hx

    maxLen=len(xList[iMax])

    #print('nb de pts dans l''invervalle choisi = '+str(maxLen))

    mx=np.mean(xList[iMax],axis=0)[0]
    my=np.mean(xList[iMax],axis=0)[1]

    irVP=c2cP((-width/2,-height/2),np.array([mx,my]))
    print('coordonnees irVP = '+str(irVP))

    #print ('temps exe = '+str(time.time()-start))

    #imgVis(drawn_img,irVP,np.array([0,0]),c1Points)

    #######################################################

    
    erPoints=[] #liste des points exterieurs

    time3_1 = time.time()
    #print("time c2cp array: "+str(time.time()-time3_1))
   # print( np.asarray(c2Points) is testPoint)
    #print(np.asarray(c2Points).shape)
    #print(testPoint.shape)
    
    
    time4 = time.time()
    for l in range(0,pointsLen):
        if(np.sqrt(c2Points[l][0]**2+c2Points[l][1]**2) >= rayon2):
            erPoints.append(c2Points[l])
    #print("time find erPoints CC: "+str(time.time()-time4))#time: 0.00938s
    
    erPointsLen=len(erPoints)

    time4_1 = time.time()
    
    #print ('nb pts ER = '+str(erPointsLen))

    #pointInterER = np.asarray(erPoints)
    time5 = time.time()
    pointInterER = np.empty(shape=[0,2])
    for k in range(0, erPointsLen):
        pointInterER = np.insert(pointInterER,pointInterER.shape[0],c2pP(erPoints[k]),axis=0)
    #print("time PointInterER PC: "+str(time.time()-time5) ) #time:0.0957s
    #print(pointInterER)


    #



    w = 0.04 #the width of bin of angle(angle coordinate)
   
    l = 30 #nb of bin in the sector we find 
    r = 1000   #sutibal radius for bound Pi of Pmax and Pmin

    m = int(2*math.pi/w)

    #pointCounter = np.empty(shape=[m])

    #count the number of point in each bin of angle and find the bin with most points
   
    time6_1 = time.time()
    pointERphi = pointInterER[:,1]
    counterPhi,bins = np.histogram(pointERphi,bins=157)
    counterERphi = counterPhi.tolist()
    #print("time to find counter angle (histogram): "+str(time.time()-time6_1)) # time: 0.000186s


    
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

    
    #print('nb de pts dans le secteur choisi = '+str(len(vpER))) 
    ##print(vpER)
    moy = np.mean(vpER, axis=0)


    #print('VP coord polaires = '+str(moy))

    vpERc2 = p2cP(moy)

    vpERc1 = c2cP((-width/2,-height/2),vpERc2)

    print ('coord erVP  = '+str(vpERc1))

    #print("time find counter radius in the sector: "+str(time.time()-time7))
#time:0.06618
    #print ('temps exe = '+str(time.time()-start))
    
    return irVP, vpERc1

