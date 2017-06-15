#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import rospy
from geometry_msgs.msg import Twist, PolygonStamped, Polygon, Point32

class PointFollow:
    
    def __init__(self):

        self.coord = Point32()
        
        self.twist_pub = rospy.Publisher ('cmd_vel_out', Twist, queue_size=1)
        self.vpCoord_sub= rospy.Subscriber('/vpCoord', PolygonStamped, self.on_vpCoord, queue_size=1)



        
    def on_vpCoord(self, ros_data):

        self.coord = ros_data.polygon.points[0]

        tw = Twist()

        if (self.coord.x < 0):
            tw.angular.z = -0.1
        else :
            tw.angular.z = 0.1
        
        self.twist_pub.publish(tw)


        
if __name__ == '__main__':
    rospy.init_node('droneCtrl', anonymous=True)
    try:
        point_follow = PointFollow()
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down vanishing/droneCtrl.py"
