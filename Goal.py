from computeVision import *
from RobotControl import *
from Vector import *
from Camera import *
import cv2
import numpy
import time
import math

cap = cv2.VideoCapture(1)
erode = (11,11)
dilation = (19,19)
blur = (21,21)
lower = np.array([31,106,150])
upper = np.array([255,255,255])
lowerGreen = np.array([0,0,0])
upperGreen = np.array([180,105,172])
TrackGoal = Track(erode_=erode,dilation_=dilation,blur_=blur,colorSpace=cv2.COLOR_BGR2LAB)
Vectorcal = Vector()
# Robot = RobotControl('COM5')

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame,0)
    shape = frame.shape
    frame = cv2.GaussianBlur(frame,(13,13),0)
    ret,listCnt,mask,contours = TrackGoal.getMaskAndCnt(frame,lower,upper)
    if ret == True:
        print 'lenliscon=', len(listCnt)
        GoalPos = TrackGoal.goal(frame,listCnt,mask)
        cv2.putText(frame,GoalPos , (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    cv2.imshow('image',frame)
    cv2.imshow('mask',mask)
    k = cv2.waitKey(10)
    if k==27:
        break

cv2.destroyAllWindows()