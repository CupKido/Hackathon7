import math
import cv2
import chooseColor
import random
import time

cameras = {}
files = {}
circles = []
ids = {}
last_id_location = {}
camera_base_angle = 145
sorted_sections = []
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
REMOVED = [set()]
NORMAL_BOX_HEIGHT = 178
SCALE_FACTOR = 0.25
BASE_CAMERA_ANGLE = 145 + 15
#PIXELS_PER_METER = 40.3
#PIXELS_PER_METER = 32.5
PIXELS_PER_METER = 26.83
BALL_SIZE = 3
WAIT_TIME = 0.15
blueprint = cv2.imread('Blueprints/Test_cases/jpg/BlueprintVectors720.jpg')
blueprint = cv2.resize(blueprint, (0, 0), fx=0.7, fy=0.7)
copy_blueprint = blueprint.copy()
delete_previous = True


def sync_params(normal_box_height, scale_factor):
    NORMAL_BOX_HEIGHT = normal_box_height
    SCALE_FACTOR = scale_factor


def add_text_data(path, capture_path, location, angle, fov, focal_length):
    capture = cv2.VideoCapture(capture_path)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    files[path] = {"frame": (width, height), "loc_params": (location, angle), "cam_params": (fov, focal_length),
                   "cap_params": capture_path, "path_params": path}
    cv2.circle(copy_blueprint, location, 10, (0, 255, 0), -1)
    cv2.imwrite('Blueprints\\Results\\blueprintLocations1.png', copy_blueprint)


def process_files():
    circle_in_files = []
    for path in files:
        circle_in_files += [process_file(path)]
    print(str(ids))
    return circle_in_files


def process_combined_files():
    path = create_combined_file()
    process_combined_file(path)

def process_combined_file(path):
    file = open(path, 'r')
    i = 0
    for line in file.readlines():
        process_combined_line(line)
        i += 1
        if i > 12:
            time.sleep(WAIT_TIME)
            i = 0

def create_combined_file():
    all_lines = []
    for path in files:
        file = open(path, 'r')
        for line in file:
            if ' ' in line:
                H, T = line.strip().split(' ', 1)
                intH = int(H) 
                if intH > 720:
                    intH -= 720
                line = str(intH) + ' ' + T
                all_lines.append((intH, line + ' ' + path))
    sorted_lines = sorted(all_lines, key=lambda x: x[0])
    pathname = 'nfile.txt'
    newfile = open(pathname,'w')
    for index, content in sorted_lines:
        newfile.write(content + ' \n')
    file.close()
    newfile.close()
    return pathname

def process_file(path):
    file = open(path, 'r')
    i = 0
    circle_in_lines = []
    for line in file.readlines():
        circle_in_lines += [process_line(line, path)]
        i += 1
        if i > 12:
            time.sleep(WAIT_TIME)
            i = 0
    return circle_in_lines


def process_combined_line(data):
    line = data.split(' ')
    if len(line) < 10:
        return
    process_line(data, line[10])

def process_combined_line(data):
    line = data.split(' ')
    if len(line) < 10:
        return
    process_line(data, line[10])

def process_line(data, path):
    name = files[path]["cap_params"]
    fov = files[path]["cam_params"][0]
    local_focal_length = int(files[path]["cam_params"][1])
    camera_angle = files[path]["loc_params"][1]
    camera_location = files[path]["loc_params"][0]
    width = int(files[path]["frame"][0])
    height = int(files[path]["frame"][1])
    line = data.split(' ')
    if len(line) < 6:
        return
    box_height = float(line[5])
    box_width = float(line[4])
    y = float(line[3])
    x = float(line[2])

    distance = (NORMAL_BOX_HEIGHT * local_focal_length) / box_height
    box_center = (x + (box_width / 2), y + (box_height / 2))
    angle = box_center[0] - (width / 2)
    angle = angle / (width / 2)
    angle = angle * (fov / 2)
    angle = math.radians(angle - (BASE_CAMERA_ANGLE - camera_angle))
    object_x = distance * math.cos(angle)
    object_y = distance * math.sin(angle)

    # find the pixel location of the object
    xLocation = camera_location[0] - (object_y * PIXELS_PER_METER)
    yLocation = camera_location[1] + (object_x * PIXELS_PER_METER)
    temp_id = int(line[1])

    if temp_id == 1 or temp_id == 9:
        temp_id = 9
    if temp_id == 3 or temp_id == 8 or temp_id == 7:
        temp_id = 8
    if temp_id == 2 or temp_id == 10:
        temp_id = 10
    # 3 and 8 and 7 - ben
    # 1 and 9 - itamar
    # 2 and 10 - saar
    if temp_id in ids.keys():
        color = ids[temp_id]
    else:
        color = chooseColor.checkForCircles(xLocation, yLocation, circles)
        if color is False:
            b = random.randint(0, 255)
            g = random.randint(0, 255)
            r = random.randint(0, 255)
            color = (b, g, r)
        ids[temp_id] = color

    print(str(temp_id) + " " + str(color) + " " + str(int(xLocation)) + " " + str(int(yLocation)))
    cv2.circle(copy_blueprint, (int(xLocation), int(yLocation)), BALL_SIZE, color, -1)
    cv2.imwrite('Blueprints\\Results\\blueprintLocations1.png', copy_blueprint)
    return int(xLocation), int(yLocation), BALL_SIZE, color


def add_camera(capture_path, location, angle, fov, focal_length):
    # capture = cv2.VideoCapture(capture_path)
    # if capture not in cameras:
    # width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # cameras[capture] = {"frame": (width, height), "loc_params": (location, angle),
    #                   "cam_params": (fov, focal_length), "cap_params": capture_path}
    # cv2.circle(copy_blueprint, location, 10, (0, 255, 0), -1)
    # cv2.imwrite('Blueprints\\Results\\blueprintLocations1.png', copy_blueprint)
    add_text_data(capture_path.split("/")[1] + ".txt", capture_path, location, angle, fov, focal_length)


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
            if delete_previous:
                copy_blueprint = blueprint.copy()
            process_frame(image, cap)
        else:
            REMOVED[0].append(cap)


def process_frame(image, cap):
    new_width = int(cameras[cap]["frame"][0] * SCALE_FACTOR)
    new_height = int(cameras[cap]["frame"][1] * SCALE_FACTOR)
    name = cameras[cap]["cap_params"]
    fov = cameras[cap]["cam_params"][0]
    local_focal_length = cameras[cap]["cam_params"][1]
    camera_angle = cameras[cap]["loc_params"][1]
    camera_location = cameras[cap]["loc_params"][0]

    image = cv2.resize(image, (new_width, new_height))
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
        distance = (NORMAL_BOX_HEIGHT * local_focal_length) / box_height

        # Calculate the angle to the object
        box_center = (x + (box_width / 2), y + (box_height / 2))
        angle = box_center[0] - (new_width / 2)
        angle = angle / (new_width / 2)
        angle = angle * (fov / 2)

        # Print the distance and angle to the object in the image and change degrees to radians
        angle = math.radians(angle - (BASE_CAMERA_ANGLE - camera_angle))
        object_x = distance * math.cos(angle)  # ------------------------------------+
        object_y = distance * math.sin(angle)  # |
        #                                                                           |
        # find the pixel location of the object                                 |------> Camera.get_person_blueprint_location(distance, angle, Map.pixels_per_meter)
        #                                                                           |
        xLocation = camera_location[0] - (object_y * PIXELS_PER_METER)  # |
        yLocation = camera_location[1] + (object_x * PIXELS_PER_METER)  # -----------+

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
    cv2.imshow(name, image)

    # write the video to a file
    # out.write(image)

    # save the blueprint image
    cv2.imwrite('Blueprints\\Results\\blueprintLocations1.png', copy_blueprint)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        REMOVED.append(cap)
