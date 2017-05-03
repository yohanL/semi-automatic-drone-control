#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

h = np.array([[0],[0],[1]])
v = np.array([[0],[1],[0]])

"""s = np.array([[[445, 37, 445, 379]]])

l = np.array([
    s[[0],[0],[1]]-s[[0],[0],[3]],
    s[[0],[0],[2]]-s[[0],[0],[0]],
    s[[0],[0],[0]]*s[[0],[0],[3]]-s[[0],[0],[2]]*s[[0],[0],[1]]
    ])

#s[[0],[0],[1]]-s[[0],[0],[3]]

#s[[0],[0],[2]]-s[[0],[0],[0]]

#s[[0],[0],[0]]*s[[0],[0],[3]]-s[[0],[0],[2]]*s[[0],[0],[1]]

#print(l.transpose().shape)
#print(v.shape)

norm = np.linalg.norm(l)

print((np.dot(l.transpose(),v))/norm)
print((np.dot(l.transpose(),h))/norm)
print()"""

s1 = np.array([[[620,450,350,250]]])
s2 = np.array([[[0,400,150,250]]])

l1 = np.array([
    s1[[0],[0],[1]]-s1[[0],[0],[3]],
    s1[[0],[0],[2]]-s1[[0],[0],[0]],
    s1[[0],[0],[0]]*s1[[0],[0],[3]]-s1[[0],[0],[2]]*s1[[0],[0],[1]]
    ])

l2 = np.array([
    s2[[0],[0],[1]]-s2[[0],[0],[3]],
    s2[[0],[0],[2]]-s2[[0],[0],[0]],
    s2[[0],[0],[0]]*s2[[0],[0],[3]]-s2[[0],[0],[2]]*s2[[0],[0],[1]]
    ])

n1 = np.linalg.norm(l1)
n2 = np.linalg.norm(l2)

print((np.dot(l1.transpose(),v))/n1)
print((np.dot(l1.transpose(),h))/n1)
print(  )
print((np.dot(l2.transpose(),v))/n2)
print((np.dot(l2.transpose(),h))/n2)

vp = l1*l2

print(vp)
