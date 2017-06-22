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

#la fonction pour detecter le point de fuite dans la region interieur et exterieur
def vp(image):

    img = image

    nbInter = 30 #nombre d'intervalles en x
    
    height = float(np.size(img, 0))
    width = float(np.size(img, 1))
    
    e1=0 #la marge d'erreur epsilon
    e2=100 #la marge d'erreur epsilon
    rayon1=float(np.sqrt(height**2+width**2)/2 + e1)
    rayon2=float(np.sqrt(height**2+width**2)/2 - e2)

    c1Points, drawn_img = findIntersection(image) #liste des points d'intersection repere cartesien 1 et l'image avec segments et points d'intersection

    pointsLen=len(c1Points)

    ################################################################### detecte le point de fuite dana la region interieur
    #transformer la coordonnee, deplaser l'origine au centre d'image 
    testPoint = np.asarray(c1Points)
    testPoint[:,0] = testPoint[:,0] - (width/2)
    testPoint[:,1] = testPoint[:,1] - (height/2)
    c2Points = testPoint.tolist()

    
    irPoints=[] #liste des points interieurs
    
    for l in range(0,pointsLen):
        if(np.sqrt(c2Points[l][0]**2+c2Points[l][1]**2) < rayon1):
            irPoints.append(c2Points[l])

    irPointsLen = len(irPoints)

    #calcule l'histogramme dans la region interieur  
    xList=[]

    for l in range(0,nbInter):
        new_list = []
        for m in range(0,irPointsLen):
            if (irPoints[m][0]>=-rayon1+2*rayon1*l/(nbInter) and irPoints[m][0]<-rayon1+2*rayon1*(l+1)/(nbInter)):
                new_list.append(irPoints[m])
        xList.append(new_list)
    

    Hx=[]


    for l in range(0,len(xList)):
        y=[]
        for k in range(0,len(xList[l])):
            y.append(xList[l][k][1])
        if (len(y)>3): #si au moins 3 points dans l'intervalle 
            Hx.append(len(xList[l])/np.var(y))
        else:
            Hx.append(0)

    iMax=Hx.index(max(Hx)) #indice max Hx

    maxLen=len(xList[iMax]) #nb de pts dans l'intervalle choisi
    #calculer les coordonnees de point de fuite qu'on trouve
    if(maxLen != 0): 
        mx=np.mean(xList[iMax],axis=0)[0]
        my=np.mean(xList[iMax],axis=0)[1]
    else:
        mx = 0
        my = 0
    #normaliser les coordonnee de point de fuite   
    if(width>height):
        irVPunit=np.array([mx/width,-my/width])
    else:
        irVPunit=np.array([mx/height,-my/height])
    
    irVP=c2cP((-width/2,-height/2),np.array([mx,my]))

    ##############################################################detecte le point de fuite dans la region exterieur

    #trouver les points d'intersection dans la region exterieur  
    erPoints=[] #liste des points exterieurs
    
    for l in range(0,pointsLen):
        if(np.sqrt(c2Points[l][0]**2+c2Points[l][1]**2) >= rayon2):
            erPoints.append(c2Points[l])

    
    erPointsLen=len(erPoints)
    
    #transfoemer la coordonnee du point a la coordonnee polaire
    pointInterER = np.empty(shape=[0,2])
    for k in range(0, erPointsLen):
        pointInterER = np.insert(pointInterER,pointInterER.shape[0],c2pP(erPoints[k]),axis=0)

    
    b=150 #nombre de bins en angle
    w=2*np.pi/b
    l = 30 #nombre de bins en rayon dans le secteur trouve 
    r = 1000   #rayon referance pour calculer le borne Pi 

    ##calcule l'histogramme de la coordonnee angle du point
    #count the number of point in each bin of angle and find the bin with most points
    pointERphi = pointInterER[:,1]
    counterPhi,bins = np.histogram(pointERphi,bins=b)
    counterERphi = counterPhi.tolist()

    #find the bin with the most point
    MaxPhi = max(counterERphi)

    indexPhi = counterERphi.index(MaxPhi)

    #count the number of point in the bin of r in the sector we have found  and find the bin with most points 

    #creat a array contain the points of the sector we find
    pointInterSector = np.empty(shape=[0,2])
    i = 0
    while i < pointInterER.shape[0]:
        if (pointInterER[[i],[1]] >= (indexPhi*w) and pointInterER[[i],[1]] < (indexPhi+1)*w):
            pointInterSector = np.insert(pointInterSector,pointInterSector.shape[0],pointInterER[i],axis=0)
        i+=1


    if (len(pointInterSector !=0)):
        Pmax = np.amax(np.amax(pointInterSector,1))
        Pmin = np.amin(np.amax(pointInterSector,1))

        phiMin = math.atan(Pmin/r)
        phiMax = math.atan(Pmax/r)


        #find the number of points in each bin
        
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
        
     
        MaxP = max(counterERp)
     
        indexP = counterERp.index(MaxP)

        ##find the candidate vanishing point

        i = 0
        vpER = np.empty(shape=[0,2])

        while i < pointInterSector.shape[0]:
            if p[indexP] < pointInterSector[i][0] < p[indexP+1]:
                vpER = np.insert(vpER,vpER.shape[0],pointInterSector[i],axis=0)
            i+=1

        moy = np.mean(vpER, axis=0)

        vpERc2 = p2cP(moy)
        
        #normalisation
        if(width>height):
            erVPunit = np.array([vpERc2[0]/width,-vpERc2[1]/width])
        else:
            erVPunit = np.array([vpERc2[0]/height,-vpERc2[1]/height])
        
        erVP = c2cP((-width/2,-height/2),vpERc2)

    else:
        
        erVP=np.empty(shape=[0,2])
        erVPunit=erVP

    print (irVPunit, erVPunit)    
    return irVP, erVP, irVPunit, erVPunit


