# functions will tell camera what color to draw on blueprint

# import the necessary packages

import numpy as np
import cv2

radius = 20

# open the blueprint image


# draw a circle on located object
def drawCircle(x, y):
    global copy_blueprint
    # check for circles in the area


# function will check for most common color in the area
def checkForCircles(x, y, circles):
    # save the amount of times a certain color is found
    colors = []

    for circle in circles:
        if (x - radius) < circle[0] < (x + radius) and (y - radius) < circle[1] < (y + radius):
            if circle[2] not in colors:
                colors.append((circle[2], 0))
            else:
                colors[colors.index(circle[2])] += 1
    if colors:
        maximum = max(colors, key=lambda item: item[1])
        return maximum[0]
    return False




