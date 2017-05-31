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

class ImageProcessing:
    
    def __init__(self):
        self.sub    = rospy.Subscriber("/image_in/compressed",  CompressedImage, self.on_image,  queue_size = 1)
        self.pub    = rospy.Publisher ("/image_out/compressed", CompressedImage,                 queue_size = 1)
        self.margin = 50
        
    def on_image(self, ros_data):

        #### From ros message to cv image ####
        compressed_in = np.fromstring(ros_data.data, np.uint8)
        image_in      = cv2.imdecode(compressed_in, cv2.IMREAD_COLOR)
        width         = image_in.shape[1]
        height        = image_in.shape[0]
        
        #### Processing ####

        p1, p2 = vp(image_in)
        image_out = imgVis(image_in,p1,p2)

        #### Publishing the result ####
        msg              = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format       = "jpeg"
        msg.data         = np.array(cv2.imencode('.jpg', image_out)[1]).tostring()
        self.pub.publish(msg)

    
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
