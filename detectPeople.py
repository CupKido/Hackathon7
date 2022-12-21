import math
import cv2

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# change hog sensitivity

cap = cv2.VideoCapture('TestVids/2Zigzag.MP4')

#open the image file blueprint.png
blueprint = cv2.imread('blueprint.png')




# Get the video's width and height
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set the scaling factor
scale_factor = 0.25
focal_length = 24
normal_box_height = 80
normal_box_width = 1
camera_location = (138,149)
pixels_per_meter = 32.5
field_of_view = 73.7
base_camera_angle = 145
camera_angle = 110
# Calculate the new width and height
new_width = int(width * scale_factor)
new_height = int(height * scale_factor)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# define out
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('straightResult.avi', fourcc, fps, (new_width, new_height))

#open the blueprint image

blueprint = cv2.imread('blueprint.png')

#resize the blueprint image

blueprint = cv2.resize(blueprint, (0,0), fx=0.7, fy=0.7)
copy_blueprint = blueprint.copy()

#draw a circle on camera location

cv2.circle(copy_blueprint, camera_location, 10, (0, 255, 0), -1)

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
            distance = (normal_box_height * focal_length) / box_height

            # Calculate the angle to the object
            box_center = (x + (box_width / 2), y + (box_height / 2))
            angle = box_center[0] - (new_width / 2)
            angle = angle / (new_width / 2)
            angle = angle * (field_of_view / 2)


            # Print the distance and angle to the object in the image and change degrees to radians
            angle = math.radians(angle - (base_camera_angle - camera_angle))
            object_x = distance * math.cos(angle)
            object_y = distance * math.sin(angle)

            #find the pixel location of the object

            xLocation = camera_location[0] - (object_y * pixels_per_meter)
            yLocation = camera_location[1] + (object_x * pixels_per_meter)

            #draw the location on the blueprint

            cv2.circle(copy_blueprint, (int(xLocation), int(yLocation)), 5, (255, 0, 0), -1)


            cv2.putText(image, "Distance: " + str(distance), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, "Angle: " + str(angle), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, "x, y: " + str(object_x) + ", " + str(object_y), (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # Showing the output Image
        cv2.imshow("Image", image)

        # write the video to a file
        out.write(image)

        #save the blueprint image
        cv2.imwrite('blueprintLocations.png', copy_blueprint)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()