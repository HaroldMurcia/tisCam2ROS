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


print("Python version:\t", sys.version)
print ("CV2 version:\t", cv2.__version__)
#camset_var="tcambin serial=26810384 ! video/x-raw, format=BGRx,width=640, height=480, framerate=30/1 ! videoconvert ! video/x-raw, format=RGB"
camset_var="v4l2src device=/dev/video6 ! video/x-raw, width=(int)1280,height=(int)960, framerate=(fraction)60/1 ! videoconvert  ! video/x-raw, format=(string)BGR ! appsink"
camset_var="tcambin serial=26810384 ! video/x-raw, width=1280, height=960, framerate=60/1 ! videoconvert ! appsink"


def image_bridge():
    image_pub = rospy.Publisher("image_topic", Image)
    rospy.init_node('image_bridge', anonymous=True)
    rate = rospy.Rate(60) # 30hz
    cam = cv2.VideoCapture(camset_var,cv2.CAP_GSTREAMER)  #,cv2.CAP_GSTREAMER
    bridge = CvBridge()
    while not rospy.is_shutdown() and cam.isOpened():
        ret,frame = cam.read()
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
    except rospy.ROSInterruptException:
        pass
