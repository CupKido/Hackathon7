import math
import cv2

import chooseColor
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
CAMERA_ANGLE = 110
#################################################################

#######################  Global variables  ######################
circles = []
#################################################################

# Initializing the HOG detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())



#######################  Video parameters  #######################

# Reading the Video from the
cap = cv2.VideoCapture('Videos/TestVids/2Zigzag.MP4')

# open the image file blueprint.png
blueprint = cv2.imread('Blueprints\\Test_cases\\png\\blueprintx T1.png')

# Get the video's width and height

# Calculate the new width and height
#fps = int(cap.get(cv2.CAP_PROP_FPS))

# define out
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('straightResult.avi', fourcc, fps, (new_width, new_height))

#################################################################


# resize the blueprint image

blueprint = cv2.resize(blueprint, (0, 0), fx=0.7, fy=0.7)
copy_blueprint = blueprint.copy()

# draw a circle on camera location

cv2.circle(copy_blueprint, CAMERA_LOCATION, 10, (0, 255, 0), -1)

while cap.isOpened():
    # Reading the video stream
    ret, image = cap.read()
    if ret:
        image = cv2.resize(image, (new_width, new_height))

        # Detecting all the regions
        # in the Image that has a
        # pedestrians inside it
        (regions, _) = hog.detectMultiScale(image,
                                            winStride=(4, 4),
                                            padding=(8, 8),
                                            scale=1.05)

        # Drawing the regions in the
        # Image
        for (x, y, w, h) in regions:
            cv2.rectangle(image, (x, y),
                          (x + w, y + h),
                          (0, 0, 255), 2)

            # Calculate the distance to the object
            box_height = h
            box_width = w
            distance = (NORMAL_BOX_HEIGHT * FOCAL_LENGTH) / box_height

            # Calculate the angle to the object
            box_center = (x + (box_width / 2), y + (box_height / 2))
            angle = box_center[0] - (new_width / 2)
            angle = angle / (new_width / 2)
            angle = angle * (FIELD_OF_VIEW / 2)

            # Print the distance and angle to the object in the image and change degrees to radians
            angle = math.radians(angle - (BASE_CAMERA_ANGLE - CAMERA_ANGLE))
            object_x = distance * math.cos(angle)
            object_y = distance * math.sin(angle)

            # find the pixel location of the object

            xLocation = CAMERA_LOCATION[0] - (object_y * PIXELS_PER_METER)
            yLocation = CAMERA_LOCATION[1] + (object_x * PIXELS_PER_METER)

            # choose color by checking other circles in the area

            color = chooseColor.checkForCircles(xLocation, yLocation, circles)
            if color is False:
                b = random.randint(0, 255)
                g = random.randint(0, 255)
                r = random.randint(0, 255)

                color = (b, g, r)

            circles.append((xLocation, yLocation, color))

            # draw the location on the blueprint

            cv2.circle(copy_blueprint, (int(xLocation), int(yLocation)), 5, color, -1)

            cv2.putText(image, "Distance: " + str(distance), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, "Angle: " + str(angle), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, "x, y: " + str(object_x) + ", " + str(object_y), (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)

        # Showing the output Image
        cv2.imshow("Image", image)

        # write the video to a file
        out.write(image)

        # save the blueprint image
        cv2.imwrite('Blueprints/Results/blueprintLocations.png', copy_blueprint)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
