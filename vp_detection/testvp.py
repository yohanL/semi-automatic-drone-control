#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from irvp import *
from ervp import *

import sys

if (int(sys.argv[1])==0): 
    irVP(sys.argv[2])
else:
    erVP(sys.argv[2])
    
