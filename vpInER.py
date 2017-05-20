#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import numpy as np
import math

pointInterPC = np.load('pointInterPC.npy')

R = 600
e = 200
w = 0.02 #the width of bin of angle(angle coordinate)
#tau = 0.01 #the width of angle bin for the bin of P(radial coordinate)
l = 100
r = 1000   #sutibal radius for bound Pi of Pmax and Pmin

n = pointInterPC.shape[0]
m = int(2*math.pi//w)

pointInterER = np.empty(shape=[0,2])
#pointCounter = np.empty(shape=[m])




##### find the ER points array

k = 0
while k < n:
    if pointInterPC[[k],[0]] > R-e:
         pointInterER = np.insert(pointInterER,pointInterER.shape[0],pointInterPC[k],axis=0)
    k+=1

#print(pointInterER.shape[0])
#print(pointInterER[[0],[1]])

###### count the number of point in each bin of angle and find the bin with most points

j = 1
counterERphi = []
pointCopyPhi = pointInterER
while j < m :
    i = 0
    c = 0
    while i < pointCopyPhi.shape[0] :
        if (pointCopyPhi[[i],[1]] >=(-math.pi+(j-1)*w) and pointCopyPhi[[i],[1]] < (-math.pi+j*w)):
            c+=1
            pointCopyPhi = np.delete(pointCopyPhi,i,axis=0)
    
            #pointCounter[j-1] = int(pointCounter[j-1])+1
           # print(pointCounter[j-1])
        else:
            i+=1
            
    counterERphi.append(c)
    j+=1
    
###the last bin of angle [-math.pi+(m-1)*w,math.pi]

i = 0
c = 0
while i < pointCopyPhi.shape[0]:
    if  (pointCopyPhi[[i],[1]] >=(-math.pi+(m-1)*w) and pointCopyPhi[[i],[1]] < (math.pi)):
         c+=1
    i+=1
counterERphi.append(c)


print(counterERphi)

###find the bin with the most point
MaxPhi = max(counterERphi)
#print(MaxPhi)

indexPhi = counterERphi.index(MaxPhi)
print(indexPhi)
print(counterERphi[indexPhi])

#####count the number of point in the bin of r in the sector we have found  and find the bin with most points 

##creat a array contain the points of the sector we find
pointInterSector = np.empty(shape=[0,2])
i = 0
while i < pointInterER.shape[0]:
    if (pointInterER[[i],[1]] >= (-math.pi+indexPhi*w) and pointInterER[[i],[1]] < (-math.pi+(indexPhi+1)*w)):
        pointInterSector = np.insert(pointInterSector,pointInterSector.shape[0],pointInterER[i],axis=0)
    i+=1
print(pointInterSector.shape)

#find Pmax,Pmin,phiMax,phiMin
Pmax = np.amax(np.amax(pointInterSector,1))
Pmin = np.amin(np.amax(pointInterSector,1))
print(Pmax)
print(Pmin)
phiMin = math.atan(Pmin/r)
phiMax = math.atan(Pmax/r)
#print(phiMin)
#print(phiMax)

###find the number of points in each bin
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
print(p)
print(counterERp)
print(len(counterERp))  
MaxP = max(counterERp)
print(MaxP)
indexP = counterERp.index(MaxP)
print(indexP)

##find the candidate vanishing point

i = 0
vpER = np.empty(shape=[0,2])
print(p[90])
print(p[91])
while i < pointInterSector.shape[0]:
    if p[indexP] < pointInterSector[i][0] < p[indexP+1]:
        vpER = np.insert(vpER,vpER.shape[0],pointInterSector[i],axis=0)
    i+=1
print(vpER)
print(vpER.shape)       


