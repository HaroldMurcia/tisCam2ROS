
#include "ros/ros.h"
// %EndTag(ROS_HEADER)%
// %Tag(MSG_HEADER)%
#include "std_msgs/String.h"
// %EndTag(MSG_HEADER)%
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

static const std::string OPENCV_WINDOW = "Image window";

using namespace std;
using namespace cv;
using namespace ros;

int main(int argc, char *argv[]){
  // ROS
  std::string videoParameter;
  std::string deviceParameter;
  std::string serialParameter;
  ros::init(argc, argv, "image_publisher");
  ros::NodeHandle nh("~");
  nh.getParam("videoParameter", videoParameter);
  nh.getParam("deviceParameter", deviceParameter);
  nh.getParam("serialParameter", serialParameter);
  ROS_INFO("Got video parameter: %s", videoParameter.c_str());
  ROS_INFO("Got device parameter: %s",deviceParameter.c_str());
  ROS_INFO("Got serial parameter: %s",serialParameter.c_str());
  image_transport::ImageTransport it(nh);
  image_transport::Publisher pub = it.advertise("camera/image", 1);
  sensor_msgs::ImagePtr msg;
  //
  // OpenCV -- Create a VideoCapture object and open the input file
  //VideoCapture cap("tcambin serial=26810384 ! video/x-raw, format=BGRx,width=(int)1280,height=(int)960, framerate=(fraction)30/1 ! videoconvert  ! video/x-raw, format=(string)BGR ! appsink", CAP_GSTREAMER);
  // default is tcambin
  //VideoCapture cap("tcambin serial=26810384 ! video/x-raw, width=1280, height=960, framerate=60/1 ! videoconvert ! appsink", CAP_GSTREAMER);
  std::string camSet = "";
  // Default Device
  std::string device_param = "/dev/video0";
  // default Serial
  std::string serial_param = "26810384";
  if (deviceParameter.compare("")!=0){
    device_param=deviceParameter.c_str();
  }
  if (serialParameter.compare("")!=0){
    serial_param=serialParameter.c_str();
  }
  if(videoParameter.compare("v4l2src")==0){
    camSet = "v4l2src device="+device_param+" ! video/x-bayer, format=(string)grbg, width=(int)1280,height=(int)960, framerate=(fraction)30/1 ! bayer2rgb ! videoconvert ! appsink";
    ROS_INFO_STREAM("\n\t video parameter = v4l2src");
  }else{
    ROS_INFO_STREAM("\n\t video parameter tcambin is default");
    camSet = "tcambin serial="+serial_param+" ! video/x-raw, width=1280, height=960, framerate=30/1 ! videoconvert ! appsink";
  }
  ROS_INFO("Camset: %s",camSet.c_str());
  VideoCapture cap(camSet, CAP_GSTREAMER);
  if(!cap.isOpened())
  {
      cout<<"VideoCapture or VideoWriter not opened"<<endl;
      exit(-1);
  }
  Mat frame;
  //
  ros::Rate loop_rate(60);
  while( nh.ok() ){
    cap.read(frame);
    // If the frame is empty, break immediately
    if (frame.empty())
      break;
    // Display the resulting frame
    //imshow( "Frame", frame );
    //to ROS
    msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", frame).toImageMsg();
    ros::Time now = ros::Time::now();
    msg->header.frame_id = "camera";
    msg->header.stamp = now;
    //
    pub.publish(msg);
    cv::waitKey(1);
    //
    ros::spinOnce();
    loop_rate.sleep();
  }

  // When everything done, release the video capture object
  cap.release();
  // Closes all the frames
  destroyAllWindows();

  return 0;
}
