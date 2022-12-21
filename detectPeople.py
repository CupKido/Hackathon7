import math
import cv2

import random
import manageCamera
############################  CONSTS  ###########################
SCALE_FACTOR = 0.25
FOCAL_LENGTH = 24
NORMAL_BOX_HEIGHT = 80
NORMAL_BOX_WIDTH = 1
CAMERA_LOCATION = (107, 144)
PIXELS_PER_METER = 32.5

FIELD_OF_VIEW = 73.7
BASE_CAMERA_ANGLE = 145
CAMERA_ANGLE = 108
#################################################################

#######################  Global variables  ######################
circles = []
#################################################################

# Initializing the HOG detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



#######################  Video parameters  #######################

# Reading the Video from the
#cap = cv2.VideoCapture('Videos/TestVids/Cam2Test2.MP4')

# open the image file blueprint.png
#blueprint = cv2.imread('Blueprints/Test_cases/blueprint.png')

# Get the video's width and height

# Calculate the new width and height
#fps = int(cap.get(cv2.CAP_PROP_FPS))

# define out
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('straightResult1.avi', fourcc, fps, (new_width, new_height))

#################################################################


# resize the blueprint image

#blueprint = cv2.resize(blueprint, (0, 0), fx=0.7, fy=0.7)
#copy_blueprint = blueprint.copy()

# draw a circle on camera location

#cv2.circle(copy_blueprint, CAMERA_LOCATION, 10, (0, 255, 0), -1)

manageCamera.sync_params(NORMAL_BOX_HEIGHT, SCALE_FACTOR)
manageCamera.add_text_data('cam2test1.txt', 'Videos/TestVids/Cam2Test1.MP4', (107, 144), CAMERA_ANGLE, FIELD_OF_VIEW, 24)
#manageCamera.add_camera('Videos/TestVids/1Zigzag.MP4', (107, 144), 145, 73.7, 24)
#manageCamera.add_camera('Videos/TestVids/Cam2Test1.MP4', (107, 144), 108, 73.7, 24)
#manageCamera.add_camera('Videos/TestVids/Cam1Test1.MP4', (211, 548), 325, 70.7, 27)
manageCamera.process_files()
#manageCamera.process_cameras()

cv2.destroyAllWindows()
