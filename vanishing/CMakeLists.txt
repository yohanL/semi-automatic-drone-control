cmake_minimum_required(VERSION 2.8.3)
project(vanishing)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  std_msgs
)
catkin_package()

catkin_install_python(PROGRAMS scripts/testvp.py scripts/vanishing_points.py scripts/conversion.py scripts/findInter.py scripts/intersection.py scripts/imgVis.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
