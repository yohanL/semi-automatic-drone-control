#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from vanishing_points import *
from imgVis import *
import sys
import numpy as np
import roslib
import rospy
from sensor_msgs.msg import CompressedImage
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats


class ImageProcessing:
    
    def __init__(self):
        self.sub    = rospy.Subscriber("/image_in/compressed",  CompressedImage, self.on_image,  queue_size = 1)
        self.pub1    = rospy.Publisher ("/image_out/compressed", CompressedImage,                 queue_size = 1)
        self.pub2    = rospy.Publisher ("/vpCoord", numpy_msg(Floats), queue_size = 1)
        self.margin = 50
        
    def on_image(self, ros_data):

        #### From ros message to cv image ####
        compressed_in = np.fromstring(ros_data.data, np.uint8)
        image_in      = cv2.imdecode(compressed_in, cv2.IMREAD_COLOR)
        
        #### Processing ####

        p1, p2, p3, p4 = vp(image_in)
        image_out = imgVis(image_in,p1,p2)
        #### Publishing image ####
        msg              = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format       = "jpeg"
        msg.data         = np.array(cv2.imencode('.jpg', image_out)[1]).tostring()
        self.pub1.publish(msg)

        #### Publishing vp coord######

        #vpCoord = np.empty(shape=[0,2])
        #vpCoord = np.insert(vpCoord,vpCoord.shape[0],p3,axis=0)
        #if(len(p4)!=0):
        #    vpCoord = np.insert(vpCoord,vpCoord.shape[0],p4,axis=0)

        if(len(p4)!=0):
            vpCoord = np.array([p3[0],p3[1],p4[0],p4[1]],dtype=np.float32)
        else:
            vpCoord = np.array([p3[0],p3[1]],dtype=np.float32)
        
        self.pub2.publish(vpCoord)

        ##########
    
if __name__ == '__main__':
    rospy.init_node('testvp', anonymous=True)
    try:
        image_processing = ImageProcessing()
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vanishing/testvp.py"

     

"""
img=cv2.imread(sys.argv[1],1)

p1,p2=vp(sys.argv[1])
cv2.imshow("vanishing points",imgVis(img,p1,p2))
cv2.waitKey(0)
"""
"""  
p1=np.array([-10,100])
p2=np.array([10,200])
cv2.imshow("vanishing points",imgVis(img,p1,p2))
cv2.waitKey(0)
"""
