#!/usr/bin/env python
# -*- coding: utf-8 -*-

#pointInterPC = np.load('pointInterPC.npy')
############


import cv2
import numpy as np
import os
from intersection import *
from conversion import *
import math

img = cv2.imread("supelecMetz.jpg",1)
grey = cv2.imread("supelecMetz.jpg",0)

height = float(np.size(img, 0))
width = float(np.size(img, 1))
taille = height*width
e=200
rayon=np.sqrt(height*height+width*width)/2 - e
edges = cv2.Canny(grey,50,150,apertureSize = 3)

cv2.imshow("Canny",edges)
cv2.waitKey(0)

"""
minLineLength = 30
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
"""

lines1 = cv2.HoughLines(edges,1,np.pi/180,200)
linesList=[]

for x in range(0, len(lines1)):
    for rho,theta in lines1[x]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = (x0 + taille*(-b))
        y1 = (y0 + taille*(a))
        x2 = (x0 - taille*(-b))
        y2 = (y0 - taille*(a))
        cv2.line(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),1)
        d=np.array([x1,y1,x2,y2])
        linesList.append(d)

cv2.imshow("Hough Transform",img)
cv2.waitKey(0)
   
#print(linesList)
#print(len(linesList))

linesLen=len(linesList)

c1Points=[] #liste des points d'intersection repere cartesien 1


for j in range(0,linesLen):
   for k in range(j+1,linesLen):
    if (linesList[j][0]!=linesList[j][2] or linesList[k][0]!=linesList[k][2]): #si au moins une des droites n'est pas verticale
        if (linesList[j][0]==linesList[j][2]): #si la 1ere droite est verticale:
            c1Points.append(getIntersectionV(linesList[j],linesList[k]))
#            print('1ere verticale')
        elif (linesList[k][0]==linesList[k][2]): #si la 2eme droite est verticale
            c1Points.append(getIntersectionV(linesList[k],linesList[j]))
#            print('2eme verticale')
        elif ( (linesList[j][3]-linesList[j][1])/(linesList[j][2]-linesList[j][0]) != (linesList[k][3]-linesList[k][1])/(linesList[k][2]-linesList[k][0]) ): #si les droites ne sont pas paralleles
            c1Points.append(getIntersection(linesList[j],linesList[k]))
#            print('pas paralleles')
#        else:
#            print('paralleles')
#    else:
#        print('deux droites verticales')
            
        
#print (c1Points)
print (len(c1Points))

pointsLen=len(c1Points)

for m in range(0,pointsLen):
    cv2.circle(img,(int(c1Points[m][0]),int(c1Points[m][1])),2,(0,0,0),-1)

                         
c2Points=[] #liste des points d'intersection repere cartesien 2

for l in range(0,pointsLen):
    c2Points.append(c2cP((width/2,height/2),c1Points[l]))

print(len(c2Points))

erPoints=[]

for l in range(0,pointsLen):
    if(np.sqrt(c2Points[l][0]*c2Points[l][0]+c2Points[l][1]*c2Points[l][1]) >= rayon):
        erPoints.append(c2Points[l])

erPointsLen=len(erPoints)
pointInterER = np.empty(shape=[0,2])

for k in range(0, erPointsLen):
    pointInterER = np.insert(pointInterER,pointInterER.shape[0],c2pP(erPoints[k]),axis=0)

#print(pointInterER)




############


w = 0.02 #the width of bin of angle(angle coordinate)
#tau = 0.01 #the width of angle bin for the bin of P(radial coordinate)
l = 30
r = 1000   #sutibal radius for bound Pi of Pmax and Pmin

m = int(2*math.pi//w)

#pointCounter = np.empty(shape=[m])




###### count the number of point in each bin of angle and find the bin with most points

j = 1
counterERphi = []
pointCopyPhi = pointInterER
while j < m :
    i = 0
    c = 0
    while i < pointCopyPhi.shape[0] :
        if (pointCopyPhi[[i],[1]] >=((j-1)*w) and pointCopyPhi[[i],[1]] < (j*w)):
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
    if  (pointCopyPhi[[i],[1]] >=((m-1)*w) and pointCopyPhi[[i],[1]] < (2*math.pi)):
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
    if (pointInterER[[i],[1]] >= (indexPhi*w) and pointInterER[[i],[1]] < (indexPhi+1)*w):
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

while i < pointInterSector.shape[0]:
    if p[indexP] < pointInterSector[i][0] < p[indexP+1]:
        vpER = np.insert(vpER,vpER.shape[0],pointInterSector[i],axis=0)
    i+=1
print(vpER)
print(vpER.shape)       


