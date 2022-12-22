import math
from datetime import datetime
from FOV_calc import *

FORMATS = {1: '35mm & FX', 2: 'DX', 3: 'CX Nikon 1'}
FORMATS = {1 : '35mm & FX', 2 : 'DX', 3 : 'CX Nikon 1'}
FPS = 24

camera_list = []

pinpoint_list = []
person_list = []

class Camera:
    """Camera Information

        Camera.id - Camera unique ID
        Camera.name - Camera name
        Camera.location - An (x, y) tuple representing the camera's location
        Camera.direction - The horizontal direction (bearing / heading) angle that the camera is facing in relation to the compass
        Camera.lens_focal_length - The Lens Focal Length, measured in mm (millimeters)
        Camera.format - Camera Format:
                            1: 35mm & FX
                            2: DX
                            3: CX Nikon 1
        Camera.horizontal_fov - The camera's field of view angle
        Camera.start_timestamp - The timestamp at which the footage started
        Camera.start_time - The time at which the footage started"""

    id: int
    name: str
    location: tuple
    direction: float
    lens_focal_length: int
    format: int
    horizontal_fov: float
    id : int
    name : str
    location : tuple
    direction : float
    lens_focal_length : int
    format : int
    horizontal_fov : float
    start_timestamp : int
    start_time : datetime

    def __init__(self, location: tuple, direction: float, lens_focal_length: int, format: int, name=''):
        return

    def __init__(self, location : tuple, direction : float, lens_focal_length : int, format : int, start_timestamp : int, name : str = ''):
        """
        location - An (x, y) tuple representing the camera's location
        direction - The horizontal direction (bearing / heading) angle that the camera is facing in relation to the compass
        lens_focal_length - The Lens Focal Length, measured in mm (millimeters)
        format - Camera Format:
                    1: 35mm & FX
                    2: DX
                    3: CX Nikon 1
        start_timestamp - The timestamp at which the footage started
        name - Camera name. If not assigned, the program will assign it as 'Camera' and the ID, for example 'Camera 1'"""
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

        if start_timestamp < 0:
            raise Exception('Timestamp must be positive')
        
        self.id = len(camera_list) + 1
        self.name = name if name != '' else f'Camera {self.id}'
        self.location = location
        self.direction = direction
        self.lens_focal_length = lens_focal_length
        self.format = format
        self.horizontal_fov = get_fov(self.lens_focal_length, self.format)[0]

        self.start_timestamp = start_timestamp
        self.start_time = datetime.fromtimestamp(self.start_timestamp)
    

    def __str__(self):
        return f'Name: {self.name}\n\
ID: {self.id}\n\
Location: x = {self.location[0]}\n\
          y = {self.location[1]}\n\
          {self.location}\n\
Direction: {self.direction}°\n\
Lens Focal Length: {self.lens_focal_length} mm\n\
Format: {FORMATS[self.format]}\n\
Max Clear View Distance: {self.max_clear_view_distance} m\n\
Horizontal FOV: {self.horizontal_fov}°\n\
Start Timestamp: {self.start_timestamp}\n\
Start Time: {self.start_time.strftime("%d/%m/%Y %H:%M:%S")}'


    def get_person_blueprint_location(self, distance : float, angle : float, pixels_per_meter : int) -> tuple:
        """Convert the location of the an object (person) on the in the frame to the location on the map"""
        object_x = distance * math.cos(angle)
        object_y = distance * math.sin(angle)

        xLocation = self.location[0] - (object_y * pixels_per_meter)
        yLocation = self.location[1] + (object_x * pixels_per_meter)

        return xLocation, yLocation



class Person:
    """Person Information
    
    Person.id - Person unique ID
    Person.name - Person name"""
    id : int
    name : str

    def __init__(self, name : str= ''):
        """
        name - Person name. If not assigned, the program will assign it as 'Person' and the ID, for example 'Person 1'"""
        self.id = len(person_list) + 1
        self.name = name if name != '' else f'Person {self.id}'


    def __str__(self):
        return f'Name: {self.name}\n\
ID: {self.id}'


    def get_points(self) -> list:
        """Gets all Pin Points related to the person"""
        return list(filter(lambda p: p.person.id == self.id, pinpoint_list))


class PinPoint:
    """Pin Point Information
    
    PinPoint.id - Pin Point unique ID
    PinPoint.person - The person that the Pin Point is representing
    PinPoint.camera - The camera from which the person was identified and pinned
    PinPoint.location - An (x, y) tuple representing the camera's location
    PinPoint.frame_number - The frame number out of all footage frames that the point has been pinned
    PinPoint.timestamp - The timestamp of when the point has been pinned
    PinPoint.time - The time of when the point has been pinned"""

    id : int
    person : Person
    camera : Camera
    location : tuple
    frame_number : int
    timestamp : int
    time : datetime

    def __init__(self, person_id : int, camera_id : int, location : tuple, frame_number : int):
        """
        person_id - The ID of the person that the Pin Point is representing
        camera_id - The ID of the camera from which the person was identified and pinned
        location - An (x, y) tuple representing the camera's location
        frame_number - The frame number out of all footage frames that the point has been pinned"""
        if person_id <= 0:
            raise Exception('Person ID must be positive')
        if person_id > len(person_list):
            raise Exception('Person with this ID does not exist')
        if camera_id <= 0:
            raise Exception('Camera ID must be positive')
        if camera_id > len(camera_list):
            raise Exception('Camera with this ID does not exist')
        if location[0] < 0 and location[1] < 0:
            raise Exception('Location x and y must be positive')
        if frame_number <= 0:
            raise Exception('Frame Number must be positive')
        
        self.id = len(pinpoint_list) + 1
        self.person = person_list[person_id - 1]
        self.camera = camera_list[camera_id - 1]
        self.location = location
        self.frame_number = frame_number
        self.timestamp = self.camera.start_timestamp + 1000 * self.frame_number / FPS
        self.time = datetime.fromtimestamp(self.start_timestamp)
    

    def __str__(self):
        return f'ID: {self.id}\n\
Person:\n\
    ID: {self.person.id}\n\
    Name: {self.person.name}\n\
Camera:\n\
    ID: {self.camera.id}\n\
    Name: {self.camera.name}\n\
Location: x = {self.location[0]}\n\
          y = {self.location[1]}\n\
          ({self.location})\n\
Frame Number: {self.frame_number}\n\
Timestamp: {self.timestamp}\n\
Time: {self.time.strftime("%d/%m/%Y %H:%M:%S")}'


    def get_person_imagename_from_frame(self) -> str:
        return f'{self.frame_number}_{self.person.id}.png' # CHECK THE FORMAT & THE FILE TYPE !!!