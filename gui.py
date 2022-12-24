import os
import tkinter as tk
from manageCamera import *
from PIL import Image, ImageTk
from FOV_calc import get_fov
import cv2

path_to_blueprint = "Blueprints\\Test_cases\\jpg\\blueprintVectors720.jpg"
path_to_vid1 = "TestVids/Cam1Test1.mp4"
path_to_vid2 = "TestVids/Cam2Test1.mp4"
circles = []
blueprint_size = (533, 633)
cameras_data_file = "appdata/cameras.txt"
fov_length = 80


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


# creating new function in canvas
tk.Canvas.create_circle = _create_circle


def draw_circle(x, y, r, **kwargs):
    canvas.create_circle(x, y, r, tag="circle", **kwargs)


def draw_camera(x, y, r, **kwargs):
    canvas.create_circle(x, y, 5, **kwargs)


def draw_camera_fov(x, y, angle):
    object_x = fov_length * math.cos(angle)
    object_y = fov_length * math.sin(angle)

    xLocation = x + object_x
    yLocation = y + object_y

    canvas.create_line(x, y, xLocation, yLocation)


def calibrate_angle(angle):
    if angle == 104:
        angle = 119

    temp = BASE_CAMERA_ANGLE - int(angle)

    return 90 - temp


def fetch_frame(eventorigin):
    closest = get_closest_circle((eventorigin.x, eventorigin.y))

    capture = cv2.VideoCapture("TestVids/New.mp4")

    # Set the current frame position to the 8th frame
    capture.set(cv2.CAP_PROP_POS_FRAMES, int(closest[4]))

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    scale_factor = 0.25

    # Read the next frame in the video
    success, frame = capture.read()

    frame = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))

    # If the frame was read successfully, display it
    if success:
        cv2.imshow("View Frame", frame)
        cv2.waitKey(0)

    capture.release()


def camera_popup(x, y):
    root = tk.Tk()

    def register_camera():
        file = open(cameras_data_file, 'a')
        angle = dir.get()
        focal = focal_length.get()
        root.destroy()
        with open(cameras_data_file, 'r+') as f:
            for line in f:
                if f"{x} {y} {angle} {get_fov(int(focal), 1)[0]} {focal}" in line:
                    print("already exist")
                    return

        if float(angle) == 104:
            file.write(f"{path_to_vid2} {x} {y} {angle} {get_fov(int(focal), 1)[0]} {focal}\n")
            add_camera(path_to_vid2, (x, y), int(angle), get_fov(int(focal), 1)[0], int(focal))
        else:
            file.write(f"{path_to_vid1} {x} {y} {angle} {get_fov(int(focal), 1)[0]} {focal}\n")
            add_camera(path_to_vid1, (x, y), int(angle), get_fov(int(focal), 1)[0], int(focal))

        fov = get_fov(int(focal), 1)[0]

        angle = calibrate_angle(angle)

        length = 60
        # draw the right edge of cam fov
        right_angle = math.radians(angle - fov / 2)
        draw_camera_fov(x, y, right_angle)

        # draw the left edge of cam fov
        left_angle = math.radians(angle + fov / 2)
        draw_camera_fov(x, y, left_angle)

    root.title("Add Camera")

    tk.Label(root, text="Direction").grid(row=0)
    tk.Label(root, text="Lens Focal Length").grid(row=1)

    dir = tk.Entry(root)
    focal_length = tk.Entry(root)

    dir.grid(row=0, column=1)
    focal_length.grid(row=1, column=1)

    submit = tk.Button(root, text="Submit", command=register_camera)
    submit.grid(row=2, column=1, sticky=tk.W)
    root.mainloop()


def add(eventorigin):
    x0 = eventorigin.x
    y0 = eventorigin.y
    draw_camera(x0, y0, 5, fill="blue")

    root.unbind("<Button 1>")

    camera_popup(x0, y0)


def add_cam():
    root.bind("<Button 1>", add)


def file_exists(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def distance2D(loc1, loc2):
    return math.sqrt((loc2[0] - loc1[0]) ** 2 + (loc2[1] - loc1[1]) ** 2)


def get_closest_circle(loc):
    if not circles:
        return -1
    min_dis = 2000000
    min_circle = ''
    for circle in circles:
        temp_loc = (circle[0], circle[1])
        distance = distance2D(temp_loc, loc)
        if distance < min_dis:
            min_dis = distance
            min_circle = circle
    return min_circle


def process_files_gui():
    global circles
    circles = process_files()
    for circle in circles:
        draw_circle(circle[0], circle[1], circle[2], fill=circle[3])


root = tk.Tk()
root.title("Main Window")

canvas = tk.Canvas(root, width=533, height=633)
canvas.pack(anchor=tk.N, expand=True)

# Load an image in the script
img = ImageTk.PhotoImage(Image.open(path_to_blueprint))

# Add image to the Canvas Items
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Add buttons to the window
add_cam = tk.Button(root, text="Add Camera", command=add_cam)
add_cam.pack()

process = tk.Button(root, text="Process Data", command=process_files_gui)
process.pack()

canvas.tag_bind("circle", "<ButtonPress-1>", fetch_frame)

if file_exists(cameras_data_file):
    with open(cameras_data_file, 'r') as f:
        for line in f:
            vid_path = line.split()[0]
            x, y, angle, fov, focal = [float(x) for x in line.split() if "mp4" not in x]

            draw_camera(x, y, 5, fill="blue")

            angle = calibrate_angle(angle)

            # draw the right edge of cam fov
            right_angle = math.radians(angle - fov / 2)
            draw_camera_fov(x, y, right_angle)

            # draw the left edge of cam fov
            left_angle = math.radians(angle + fov / 2)
            draw_camera_fov(x, y, left_angle)
            print(line)

root.mainloop()
