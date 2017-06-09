#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
from intersection import *
from conversion import *
from imgVis import *
import math
import time

def findIntersection(image):

    img = image
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    longueur = 20 #longueur pour eliminer segments courts
    height = float(np.size(img, 0))
    width = float(np.size(img, 1))

    lsd = cv2.createLineSegmentDetector(0)
    lines = lsd.detect(grey)[0]
    linesLen=(lines.shape[0])

    j=0
    while (j<linesLen): #boucle pour eliminer les segments courts
        x1 = lines[[j],[0],[0]]
        y1 = lines[[j],[0],[1]]
        x2 = lines[[j],[0],[2]]
        y2 = lines[[j],[0],[3]]
        if ((math.sqrt((x1-x2)**2+(y1-y2)**2)<longueur) or (math.degrees(math.atan(abs((x1-x2)/(y1-y2)))) < 3) ):
            lines = np.delete(lines,j,0)
            linesLen-=1
        else:
            j+=1
        
    drawn_img = lsd.drawSegments(img,lines)
    #drawn_img = img
    
    linesList = np.squeeze(lines)

    #print('nb lignes = '+str(linesLen))

    c1Points=[] #liste des points d'intersection repere cartesien 1

    for j in range(0,linesLen):
        for k in range(j+1,linesLen):
            if (linesList[j][0]!=linesList[j][2] or linesList[k][0]!=linesList[k][2]): #si au moins une des droites n'est pas verticale
                if (linesList[j][0]==linesList[j][2]): #si la 1ere droite est verticale:
                    c1Points.append(getIntersectionV(linesList[j],linesList[k]))
                elif (linesList[k][0]==linesList[k][2]): #si la 2eme droite est verticale
                    c1Points.append(getIntersectionV(linesList[k],linesList[j]))
                elif ( (linesList[j][3]-linesList[j][1])/(linesList[j][2]-linesList[j][0]) != (linesList[k][3]-linesList[k][1])/(linesList[k][2]-linesList[k][0]) ): #si les droites ne sont pas paralleles
                    c1Points.append(getIntersection(linesList[j],linesList[k]))          

    pointsLen=len(c1Points)
    #print ('nb pts intersection = '+str(pointsLen))

    """
    for m in range(0,pointsLen): #on dessine les points d'intersection
        cv2.circle(drawn_img,(int(c1Points[m][0]),int(c1Points[m][1])),2,(0,0,0),-1)
    """
    
    return c1Points, drawn_img
