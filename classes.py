import math
from FOV_calc import *

FORMATS = {1: '35mm & FX', 2: 'DX', 3: 'CX Nikon 1'}

camera_list = []


class Camera:
    """Camera InformationP
    
        Camera.location - An (x, y) tuple representing the camera's location
        Camera.direction - The horizontal direction (bearing / heading) angle that the camera is facing in relation to the compass
        Camera.lens_focal_length - The Lens Focal Length, measured in mm (millimeters)
        Camera.format - Camera Format:
                            1: 35mm & FX
                            2: DX
                            3: CX Nikon 1
        Camera.max_clear_view_distance - The maximum distance, measured in meters, at which the camera can clearly recognize an object"""

    id: int
    name: str
    location: tuple
    direction: float
    lens_focal_length: int
    format: int
    horizontal_fov: float

    def __init__(self, location: tuple, direction: float, lens_focal_length: int, format: int, name=''):
        if location[0] < 0 and location[1] < 0:
            raise Exception('Location x and y must be positive')
        if not 0 <= direction <= 360:
            raise Exception('Direction must be between 0 and 360')
        if lens_focal_length < 0:
            raise Exception('Lens Focal Length must be positive')
        if lens_focal_length not in (
        10, 11, 12, 14, 15, 17, 18, 19, 20, 24, 28, 30, 35, 45, 50, 55, 60, 70, 75, 80, 85, 90, 100, 105, 120, 125, 135,
        150, 170):
            raise Exception('Lens Focal Length is not supported')
        if format not in (1, 2, 3):
            raise Exception('Format is not supported')

        self.id = len(camera_list) + 1
        self.name = name if name != '' else f'Camera {self.id}'
        self.location = location
        self.direction = direction
        self.lens_focal_length = lens_focal_length
        self.format = format
        self.horizontal_fov = get_fov(self.lens_focal_length, self.format)[0]

    def __str__(self):
        return f'Name: {self.name}\n\
ID: {self.id}\n\
Location: x = {self.location[0]}\n\
          y = {self.location[1]}\n\
          {self.location}\n\
Direction: {self.direction}°\n\
Lens Focal LengthL: {self.lens_focal_length} mm\n\
Format: {FORMATS[self.format]}\n\
Horizontal FOV: {self.horizontal_fov}°'

    def get_person_blueprint_location(self, distance: float, angle: float, pixels_per_meter: int) -> tuple:
        object_x = distance * math.cos(angle)
        object_y = distance * math.sin(angle)

        xLocation = self.location[0] - (object_y * pixels_per_meter)
        yLocation = self.location[1] + (object_x * pixels_per_meter)

        return xLocation, yLocation
