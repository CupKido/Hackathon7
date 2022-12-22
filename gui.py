import math
import tkinter as tk
from manageCamera import BASE_CAMERA_ANGLE, process_frames, add_camera, PIXELS_PER_METER
from PIL import Image, ImageTk
from classes import Camera
from FOV_calc import get_fov

path_to_blueprint = "Blueprints/Templates/png/Israel_Floor_2.png"
path_to_vid1 = "TestVids/Cam1Test2.mp4"
path_to_vid2 = "TestVids/Cam2Test2.mp4"


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


def camera_popup(x, y):
    root = tk.Tk()

    def register_camera():
        angle = dir.get()
        focal = focal_length.get()

        if float(angle) == 109:
            add_camera(path_to_vid2, (x, y), angle, get_fov(int(focal), 1)[0], focal)
        else:
            add_camera(path_to_vid1, (x, y), angle, get_fov(int(focal), 1)[0], focal)
        root.quit()

        fov = get_fov(int(focal), 1)[0]

        temp = BASE_CAMERA_ANGLE - int(angle)

        angle = temp if temp % 90 else 90 - temp

        length = 60
        # draw the right edge of cam fov
        right_angle = math.radians(angle - fov / 2)

        object_x = length * math.cos(right_angle)
        object_y = length * math.sin(right_angle)

        xLocation = x + object_x
        yLocation = y + object_y

        canvas.create_line(x, y, xLocation, yLocation)

        # draw the left edge of cam fov
        left_angle = math.radians(angle + fov / 2)

        object_x = length * math.cos(left_angle)
        object_y = length * math.sin(left_angle)

        xLocation = x + object_x
        yLocation = y + object_y

        canvas.create_line(x, y, xLocation, yLocation)

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
    canvas.create_circle(x0, y0, 5, fill="blue", outline="", width=4)

    camera_popup(x0, y0)

    root.unbind("<Button 1>")


def add_cam():
    root.bind("<Button 1>", add)


tk.Canvas.create_circle = _create_circle

blueprint_size = (588, 712)

root = tk.Tk()
root.title("Main Window")

canvas = tk.Canvas(root, width=600, height=650)
canvas.pack(anchor=tk.N, expand=True)

# Load an image in the script
img = ImageTk.PhotoImage(Image.open(path_to_blueprint))

# Add image to the Canvas Items
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Add buttons to the window
add_cam = tk.Button(root, text="Add Camera", command=add_cam)
add_cam.pack()

process = tk.Button(root, text="Process Data", command=process_frames)
process.pack()


def run():
    root.mainloop()


run()
