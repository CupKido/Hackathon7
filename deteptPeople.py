import cv2
import imutils

# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cap = cv2.VideoCapture('video.mp4')

# Get the video's width and height
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set the scaling factor
scale_factor = 0.25

# Calculate the new width and height
new_width = int(width * scale_factor)
new_height = int(height * scale_factor)

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

        # Showing the output Image
        cv2.imshow("Image", image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
