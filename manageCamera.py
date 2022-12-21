import math
import cv2
import chooseColor
import random
cameras = {}
circles = []
camera_base_angle = 145
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
REMOVED = [set()]
NORMAL_BOX_HEIGHT = 80
SCALE_FACTOR = 0.25
BASE_CAMERA_ANGLE = 145
PIXELS_PER_METER = 32.5
blueprint = cv2.resize(cv2.imread('Blueprints/Test_cases/blueprint.png'), (0, 0), fx=0.7, fy=0.7)
copy_blueprint = blueprint.copy()


def sync_params(normal_box_height, scale_factor):
    NORMAL_BOX_HEIGHT = normal_box_height
    SCALE_FACTOR = scale_factor
    


def add_camera(capture_path, location, angle, fov, focal_length):
    capture = cv2.VideoCapture(capture_path)
    if(capture not in cameras):
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cameras[capture] = {"frame" : (width, height) , "loc_params" : (location, angle), "cam_params" : (fov, focal_length), "cap_param" : capture_path}

def remove_cameras():
    if REMOVED[0]:
        for capture in REMOVED[0]:
            if capture in cameras and capture is not None or True:
                cameras.pop(capture)
                capture.release()
    REMOVED[0] = set()

def check_camera_open():
    flag = False
    for cap in cameras:
        if cap.isOpened():
            flag = True
        else:
            REMOVED[0].append(cap)
    remove_cameras()
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
            REMOVED[0].append(cap)


def process_frame(image, cap):
    image = cv2.resize(image, (int(cameras[cap]["frame"][0] * SCALE_FACTOR), int(cameras[cap]["frame"][1] * SCALE_FACTOR)))

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
        distance = (NORMAL_BOX_HEIGHT * cameras[cap]["cam_params"][0]) / box_height

            # Calculate the angle to the object
        box_center = x + (box_width / 2)
        image_center = cameras[cap]["frame"][0] / 2
        angle = (box_center - image_center) / image_center
        angle = angle * 180 / math.pi

        # Print the distance and angle to the object in the image
        angle = math.radians(angle - (BASE_CAMERA_ANGLE - cameras[cap]["cam_params"][1]))
        object_x = distance * math.cos(angle)
        object_y = distance * math.sin(angle)

        xLocation = cameras[cap]["loc_params"][0][0] - (object_y * PIXELS_PER_METER)
        yLocation = cameras[cap]["loc_params"][0][1] + (object_x * PIXELS_PER_METER)

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
    cv2.imshow(str(cameras[cap]["cap_param"]), image)
    cv2.imwrite('Blueprints\\Results\\blueprintLocations1.png', copy_blueprint)
    # write the video to a file
    #detectPeople.out.write(image)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        REMOVED[0].append(cap)
