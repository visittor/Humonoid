import cv2
import numpy as np
from computeVision import *

cap = cv2.VideoCapture(0)
cv2.namedWindow('set')
def nothing():
    pass
cv2.createTrackbar('1', 'set', 0, 255,nothing)
cv2.createTrackbar('2', 'set', 0, 255, nothing)
cv2.createTrackbar('3', 'set', 0, 255, nothing)
cv2.createTrackbar('4', 'set', 0, 255, nothing)
cv2.createTrackbar('5', 'set', 0, 255, nothing)
cv2.createTrackbar('6', 'set', 0, 255, nothing)
while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,0)
    frame = cv2.GaussianBlur(frame,(13,13),0)
    lab = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    H1 = cv2.getTrackbarPos('1', 'set')
    H2 = cv2.getTrackbarPos('2', 'set')
    S1 = cv2.getTrackbarPos('3', 'set')
    S2 = cv2.getTrackbarPos('4', 'set')
    V1 = cv2.getTrackbarPos('5', 'set')
    V2 = cv2.getTrackbarPos('6', 'set')
    lower = np.array([H1,S1,V1])
    upper = np.array([H2,S2,V2])
    mask = cv2.inRange(lab,lower,upper)
    mask = removeNoise(mask,(7,7),(7,7),(21,21))
    # circle = cv2.HoughCircles(frame[:, :, 2], cv2.HOUGH_GRADIENT, 1, 20, param1=85, param2=40, minRadius=0,
    #                           maxRadius=500)
    # if circle is not None:
    #     print 'a'
    #     for i in circle[0, :]:
    #         cv2.circle(frame, (i[0], i[1]), i[2], (0, 0, 0), 2)

    cv2.imshow('mask',mask)
    cv2.imshow('frame',frame)
    cv2.imshow('L',frame[:,:,0])
    cv2.imshow('A', frame[:, :, 1])
    cv2.imshow('B', frame[:, :, 2])
    # stack = np.hstack((frame, mask))
    # cv2.imshow('window',stack)
    k = cv2.waitKey(10)
    if k == 27:
        break

cv2.destroyAllWindows()