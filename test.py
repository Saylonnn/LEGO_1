import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time
#link https://stackoverflow.com/questions/56875876/detect-circles-with-specific-colors-using-opencv

cap = cv.VideoCapture('1.mp4')
template_green = cv.imread('PC\PatternPics\GreenBall.jpg', -1)
cv.imshow('Green Template', template_green)

if (cap.isOpened() == False):
    print("Error opening Video stream or file.")

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        '''
        result = cv.matchTemplate(frame, template_green, cv.TM_CCORR_NORMED)
        (minVal, maxVal, minLoc, maxLoc)= cv.minMaxLoc(result)
        top_left = minLoc
        bottom_right = (top_left[0] + 50, top_left[1] + 50)
        
        cv.rectangle(frame,top_left, bottom_right, (255, 0, 0), 3)
        '''

        lower_blue = np.array([80, 60, 30])
        upper_blue = np.array([100, 90, 50])

        mask = cv.inRange(frame, lower_blue, upper_blue)
        res = cv.bitwise_and(frame, frame, mask=mask)

        cv.imshow('mask', mask)
        cv.imshow('Frame', frame)
        cv.imshow('res', res)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break