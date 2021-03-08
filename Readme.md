# tisCam2ROS
This repository is an attempt to bring the data from a TheImagingSource DFM 27UR0135-M camera to ROS using cpp and opencv with [cv_bridge](http://wiki.ros.org/cv_bridge). Since GSCAM the tcambin needs GStreamer 1.0. and as far as I know,GSCAM, which uses a different GStreamer.

##### MENU
[Hardware](#hardware)
[How to install](#how2install)
[How to use](#how2use)


<a name="hardware"/>

## 1. Hardware

USB 3.0 RGB BOARD CAMERA: [The Imaging Source DFM 27UR0135-ML](https://www.theimagingsource.com/products/board-cameras/usb-3.0-color/dfm27ur0135ml/)
* 1/3 inch On Semiconductor CMOS sensor (AR0135)
* 1,280×960 (1.2 MP), up to 60 fps
* Global shutter
* Trigger and I/O inputs
* Manufactured by The Imaging Source

Identifies device and formats:
```console
$ sudo apt-get install v4l-utils
$ ls /dev/video*
$ v4l2-ctl --list-devices
```
Example dev 0
```console
$ v4l2-ctl --list-formats-ext -d 0
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture

	[0]: 'GRBG' (8-bit Bayer GRGR/BGBG)
		Size: Discrete 1280x960
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.020s (50.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.013s (80.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.020s (50.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 1024x768
			Interval: Discrete 0.013s (80.000 fps)
			Interval: Discrete 0.014s (70.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 640x480
			Interval: Discrete 0.008s (120.000 fps)
			Interval: Discrete 0.011s (90.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
	[1]: 'GREY' (8-bit Greyscale)
		Size: Discrete 1280x960
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.020s (50.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.013s (80.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.020s (50.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 1024x768
			Interval: Discrete 0.013s (80.000 fps)
			Interval: Discrete 0.014s (70.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 640x480
			Interval: Discrete 0.008s (120.000 fps)
			Interval: Discrete 0.011s (90.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
	[2]: 'Y16 ' (16-bit Greyscale)
		Size: Discrete 1280x960
			Interval: Discrete 0.014s (70.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.020s (50.000 fps)
			Interval: Discrete 0.025s (40.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.050s (20.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 640x480
			Interval: Discrete 0.008s (120.000 fps)
			Interval: Discrete 0.011s (90.000 fps)
			Interval: Discrete 0.017s (60.000 fps)
			Interval: Discrete 0.033s (30.000 fps)
			Interval: Discrete 0.067s (15.000 fps)
			Interval: Discrete 0.100s (10.000 fps)
$ v4l2-ctl -d /dev/video0 --get-fmt-video
Format Video Capture:
	Width/Height      : 1280/960
	Pixel Format      : 'GRBG' (8-bit Bayer GRGR/BGBG)
	Field             : None
	Bytes per Line    : 1280
	Size Image        : 1228800
	Colorspace        : Default
	Transfer Function : Default (maps to Rec. 709)
	YCbCr/HSV Encoding: Default (maps to ITU-R 601)
	Quantization      : Default (maps to Full Range)
	Flags             : 
```
Test VideoDevice:
```console
$ gst-launch-1.0 tcambin device=/dev/video0 ! 'video/x-raw,format=BGRx,width=1280,height=960,framerate=60/1' ! videoconvert ! autovideosink
$ gst-launch-1.0 tcambin device=/dev/video0 ! video/x-raw, width=1280, height=960, framerate=60/1 ! videoconvert ! autovideosink
```

<a name="how2install"/>

## 2. How to install

Install opencv2
```console
$ sudo apt update
$ sudo apt install libopencv-dev python3-opencv
$ python3 -c "import cv2; print(cv2.__version__)"
$ sudo apt install build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev libopenexr-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
$ sudo apt-get install ros-melodic-video-stream-opencv
$ sudo apt install ffmpeg
```
Install [TIS Camera](https://www.theimagingsource.com/documentation/tiscamera/tutorial.html): 
```console
$ git clone https://github.com/TheImagingSource/tiscamera
$ cd tiscamera
$ mkdir build
$ ./scripts/dependency-manager install
$ make -j
```
Clone repo in ~/catkin_ws/src
```console
$ git clone https://github.com/HaroldMurcia/tisCam2ROS
$ cd ../..
$ catkin_make
```

<a name="how2use"/>

## 3. How to use

**Todo**:
* To find a configuration that allows the use of true colors and 60 FPS sample rate:
    * Option 1: 50 FPS, with color distortion "VideoCapture cap("v4l2src device=/dev/video6 ! video/x-bayer, format=(string)grbg, width=(int)1280,height=(int)960, framerate=(fraction)60/1  ! bayer2rgb ! videoconvert  ! appsink", CAP_GSTREAMER);"
    * Option 2: 27 FPS, without color distortion; "VideoCapture cap("tcambin serial=26810384 ! video/x-raw, width=1280, height=960, framerate=60/1 ! videoconvert ! appsink", CAP_GSTREAMER);"

to execute v4l2src use:
```console
$ rosrun tisCam2ROS tisCam2ROS_node _videoParameter:=v4l2src _deviceParameter:=/dev/video6
```

to execute tcambin use:
```console
$ rosrun tisCam2ROS tisCam2ROS_node _videoParameter:=tcambin _serialParameter:=26810384
```