#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

#D : droite
#P : point

def p2cD(line): #line : array (rho,theta)
    rho=(line[0])
    theta=line[1]
    if (theta==float(0)):
        a=1
        b=0
        c=-rho
    else:
        a1=-1/np.tan(rho) #paramètres de l'équation réduite
        b1=rho/np.sin(theta)
        b=1
        a=-a1*b
        c=-b1*b
    return np.array([a,b,c])

def c2cP(newO, point): #new0 = (-width/2,-height/2)
    x=point[0]-newO[0]
    y=point[1]-newO[1]
    return np.array([x,y])

def c2pP(point): 
    x=point[0]
    y=point[1]
    rho=np.sqrt(x*x+y*y)
    if(x>0 and y>=0):
        theta=np.arctan(y/x)
    elif(x>0 and y<0):
        theta=np.arctan(y/x)+2*np.pi
    elif(x<0):
        theta=np.arctan(y/x)+np.pi
    elif(x==0 and y>0):
        theta=np.pi/2
    elif(x==0 and y<0):
        theta=-np.pi/2
    return np.array([rho,theta])
    
def p2cP(point):
    rho=point[0]
    theta=point[1]
    x=rho*np.cos(theta)
    y=rho*np.sin(theta)
    return np.array([x,y])
