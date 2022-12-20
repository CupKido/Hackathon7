import math
import cv2

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture('TestVids/2Zigzag.MP4')

# Get the video's width and height
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set the scaling factor
scale_factor = 0.25
focal_length = 24
normal_box_height = 80
normal_box_width = 1

# Calculate the new width and height
new_width = int(width * scale_factor)
new_height = int(height * scale_factor)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# define out
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, fps, (new_width, new_height))

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
                                            padding=(4, 4),
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
            box_center = x + (box_width / 2)
            image_center = new_width / 2
            angle = (box_center - image_center) / image_center
            angle = angle * 180 / math.pi

            # Print the distance and angle to the object in the image

            cv2.putText(image, "Distance: " + str(distance), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, "Angle: " + str(angle), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Showing the output Image
        cv2.imshow("Image", image)

        # write the video to a file
        out.write(image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()