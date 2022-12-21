import cv2

#open the blueprint image

blueprint = cv2.imread('blueprint.png')

#resize the blueprint image

blueprint = cv2.resize(blueprint, (0,0), fx=0.7, fy=0.7)

global xPosition, yPosition

#write function that saves mouse click coordinates

def savePosition(event,x,y,flags,param):

    global xPosition, yPosition

    if event == cv2.EVENT_LBUTTONDOWN:
        print (x,y)
        #draw a circle on camera location
        cv2.circle(blueprint, (x, y), 10, (0, 255, 0), -1)


#set mouse callback function

cv2.namedWindow('blueprint')
cv2.setMouseCallback('blueprint', savePosition)


while True:

    cv2.imshow('blueprint', blueprint)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break