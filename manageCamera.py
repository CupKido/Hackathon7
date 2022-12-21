import detectPeople
import math
cameras = {}
camera_base_angle = 145
hog = None
cv2 = None
def sync_params():
    hog = detectPeople.hog
    cv2 = detectPeople.cv2


def add_camera(capture, location, angle):
    if(capture not in cameras):
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cameras[capture] = {"frame" : (width, height) , "loc_params" : (location, angle)}


def check_camera_open():
    flag = False
    for cap in cameras:
        if cap.isOpened():
            flag = True
        else:
            cameras -= cap
    return flag

def process_cameras(): 
    while check_camera_open():
        process_frames()


def process_frames():
    for cap in cameras:
        ret, image = cap.read()
        if ret:
            process_frame(image, cap)
        else:
            cameras -= cap


def process_frame(image, cap):
    image = cv2.resize(image, (new_width, new_height))

    # Detecting all the regions
    # in the Image that has a
    # pedestrians inside it
    (regions, _) = hog.detectMultiScale(image,winStride=(4, 4),padding=(4, 4),scale=1.05)

        # Drawing the regions in the
        # Image
    for (x, y, w, h) in regions:
        cv2.rectangle(image, (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)

            # Calculate the distance to the object
        box_height = h
        box_width = w
        distance = (detectPeople.normal_box_height * detectPeople.focal_length) / box_height

            # Calculate the angle to the object
        box_center = x + (box_width / 2)
        image_center = detectPeople.new_width / 2
        angle = (box_center - image_center) / image_center
        angle = angle * 180 / math.pi

        # Print the distance and angle to the object in the image

        object_x = distance * math.cos(angle)
        object_y = distance * math.sin(angle)

        cv2.putText(image, "Distance: " + str(distance), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(image, "Angle: " + str(angle), (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(image, "x, y: " + str(object_x) + ", " + str(object_y), (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # Showing the output Image
    cv2.imshow("Image", image)

        # write the video to a file
    detectPeople.out.write(image)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cameras -= cap
