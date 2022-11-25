from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

from gopigo import *
import sys

import atexit
atexit.register(stop)


from picamera.array import PiRGBArray # Generates a 3D RGB array
from picamera import PiCamera # Provides a Python interface for the RPi Camera Module
import time # Provides time-related functions
import cv2 # OpenCV library

print("Initial values encoders L: %6d  R: %6d" % (enc_read(0), enc_read(1)))

print("Moving motors for a bit")
fwd()
time.sleep(3)
stop()
print("New values encoders L: %6d  R: %6d" % (enc_read(0), enc_read(1)))
print("Testing camera, press q to quit")

# Initialize the camera
camera = PiCamera()
 
# Set the camera resolution
camera.resolution = (640, 480)
 
# Set the number of frames per second
camera.framerate = 32
 
# Generates a 3D RGB array and stores it in rawCapture
raw_capture = PiRGBArray(camera, size=(640, 480))
 
# Wait a certain number of seconds to allow the camera time to warmup
time.sleep(0.1)
 
# Capture frames continuously from the camera
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
     
    # Grab the raw NumPy array representing the image
    image = frame.array
     
    # Display the frame using OpenCV
    cv2.imshow("Frame", image)
     
    # Wait for keyPress for 1 millisecond
    key = cv2.waitKey(1) & 0xFF
     
    # Clear the stream in preparation for the next frame
    raw_capture.truncate(0)
     
    # If the `q` key was pressed, break from the loop
    if key == ord("q"):
        break