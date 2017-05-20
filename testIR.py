import cv2
import numpy as np
import os
from intersection import *
from conversion import *
import math

img = cv2.imread("couloir3.jpg",1)
grey = cv2.imread("couloir3.jpg",0)

height = float(np.size(img, 0))
width = float(np.size(img, 1))
taille = height*width
e=200
r=np.sqrt(height*height+width*width)/2 + e
edges = cv2.Canny(grey,50,150,apertureSize = 3)

cv2.imshow("Canny",edges)
cv2.waitKey(0)

"""
minLineLength = 30
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
"""

lines1 = cv2.HoughLines(edges,1,np.pi/180,170)
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

irPoints=[]

for l in range(0,pointsLen):
    if(np.sqrt(c2Points[l][0]*c2Points[l][0]+c2Points[l][1]*c2Points[l][1]) < r):
        irPoints.append(c2Points[l])


print(len(irPoints))
irPointsLen = len(irPoints)

nbInter=20
xList=[]
for l in range(0,nbInter):
    new_list = []
    for m in range(0,irPointsLen):
        if (irPoints[m][0]>=-r+2*r*l/(nbInter) and irPoints[m][0]<-r+2*r*(l+1)/(nbInter)):
            new_list.append(irPoints[m])
    xList.append(new_list)
    
#print(len(xList))

#for l in range(0,len(xList)):
#    print(len(xList[l]))

print()
Hx=[]

for l in range(0,len(xList)):
    y=[]
    for k in range(0,len(xList[l])):
        y.append(xList[l][k][1])
    if (len(y)>1): #si au moins 2 points dans l'intervalle
        Hx.append(len(xList[l])/np.var(y))
    else:
        Hx.append(0)

#print(Hx)

iMax=Hx.index(max(Hx))
print(iMax)

maxLen=len(xList[iMax])
mx=0
my=0
for k in range(0, maxLen):
    mx=mx+xList[iMax][k][0]/maxLen
for k in range(0, maxLen):
    my=my+xList[iMax][k][1]/maxLen

print(mx)
print(my)

irVP=c2cP((-width/2,-height/2),np.array([mx,my]))
print(irVP)

cv2.circle(img,(int(irVP[0]),int(irVP[1])),5,(0,255,0),-1)

"""
pPoints=[]

for l in range(0,pointsLen):
    pPoints.append(c2pP(c2Points[l]))
    
print(pPoints)
print(len(pPoints))
"""
######





cv2.imshow("Hough Transform",img)
cv2.waitKey(0)
