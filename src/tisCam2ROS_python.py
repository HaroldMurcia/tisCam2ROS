#!/usr/bin/env python3
import os
import sys
import cv2
import time
import ast
from datetime import datetime
from pathlib import Path
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import gi

print("Python version:\t", sys.version)
print ("CV2 version:\t", cv2.__version__)
#camset_var="v4l2src device=/dev/video0 ! video/x-raw, format=BGRx,width=1280, height=960, framerate=30/1 ! videoconvert ! appsink"
#camset_var="v4l2src device=/dev/video0 ! video/x-raw, width=(int)1280,height=(int)960, framerate=(fraction)60/1 ! videoconvert  ! video/x-raw, format=(string)BGR ! appsink"
#camset_var="tcambin serial=26810384 ! video/x-raw, width=1280,height=960, framerate=30/1 ! videoconvert ! appsink"
camset_var="tcambin serial=26810384 ! video/x-raw, format=BGRx, width=640,height=480, framerate=60/1 ! videoconvert ! appsink"
#cam = cv2.VideoCapture(camset_var,cv2.CAP_GSTREAMER)
cam = cv2.VideoCapture(camset_var,cv2.CAP_GSTREAMER)
print("open?",cam.isOpened())
cam.release()

print(camset_var)
def image_bridge():
    image_pub = rospy.Publisher("image_topic", Image, queue_size=10)
    rospy.init_node('image_bridge', anonymous=True)
    rate = rospy.Rate(60)
    cam = cv2.VideoCapture(camset_var,cv2.CAP_GSTREAMER)
    #cam.set(cv2.CAP_PROP_FPS, 60)
    #cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    #cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('G','R','B','G'))
    #cam.set(cv2.CAP_PROP_CONVERT_RGB, True)
    #print(cam.get(cv2.CAP_PROP_AUTO_EXPOSURE))
    #print(cam.get(cv2.CAP_PROP_FORMAT))
    #print(cam.get(cv2.CAP_PROP_MODE))
    #print(cam.get(cv2.CAP_PROP_CONVERT_RGB))
    bridge = CvBridge()
    while not rospy.is_shutdown() and cam.isOpened():
        ret,frame = cam.read()
        cv2.imwrite('capture.png', frame)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BayerGR2BGR)
        image_message = bridge.cv2_to_imgmsg(frame, "passthrough")
        image_pub.publish(image_message)
        #cv2.imshow('img',frame)
        rate.sleep()
        if cv2.waitKey(1)==ord('q'):
            break
    cam.release()
    del cam


if __name__ == '__main__':
    try:
        image_bridge()
        print("Hola")
    except rospy.ROSInterruptException:
        pass
