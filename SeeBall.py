import cv2
import numpy as np
from computeVision import *
from RobotControl import *
import time
import math
from Camera import *

cap = cv2.VideoCapture(1)
erode = (7,7)
dilation = (7,7)
blur = (21,21)
lower = np.array([31,106,150])
upper = np.array([255,255,255])
# lower = np.array([0,167,0])
# upper = np.array([40,255,255])
lowerGreen = np.array([0,0,0])
upperGreen = np.array([203,105,172])
TrackBall = Track(erode_=erode,dilation_=dilation,blur_=blur,shape_=(1,10),colorSpace=cv2.COLOR_BGR2LAB)

# Robot = RobotControl('/dev/ttyUSB1')
Robot = RobotControl('COM6')
angle = [2046,2046]
# Robot.goCenter()
Robot.movemotor(42, 2045, 1023)
Robot.movemotor(41, 2046, 1023)
Robot.movemotor(1, 1980, 1023)
Robot.movemotor(2, 2090, 1023)
Robot.movemotor(3, 2910, 1023)
Robot.movemotor(4, 546, 1023)
Robot.movemotor(5, 1390, 1023)
Robot.movemotor(6, 2090, 1023)
Robot.movemotor(11, 1980, 1023)
Robot.movemotor(12, 2090, 1023)
Robot.movemotor(13, 2910, 1023)
Robot.movemotor(14, 546, 1023)
Robot.movemotor(15, 1390, 1023)
Robot.movemotor(16, 2090, 1023)
Robot.movemotor(31, 1770, 1023)
Robot.movemotor(32, 1540, 1023)
Robot.movemotor(33, 2046, 1023)
Robot.movemotor(21, 1770, 1023)
Robot.movemotor(22, 1540, 1023)
Robot.movemotor(23, 2046, 1023)
time.sleep(0.05)
listDifH = []
listDifV = []

FOV = findFieldOfView(60,28,102.5,60)

while True:
    start = time.time()
    ret,frame = cap.read()
    frameCenter = (frame.shape[1]/2,frame.shape[0]/2)
    frame = cv2.flip(frame, 0)
    frame = cv2.GaussianBlur(frame,(13,13),0)

    maskGreen = TrackBall.getOnlyMask(frame,lowerGreen,upperGreen)
    _,c,_ = cv2.findContours(maskGreen.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(maskGreen,c[:],-1,255,-1)
    notMaskGreen = cv2.bitwise_not(maskGreen)
    ret,Cnt,mask,Allcontours = TrackBall.getMaskAndCnt(frame,lower,upper,percen=0.035,dst=maskGreen)
    isContour,Maxcontour = TrackBall.chooseOne(Cnt,Allcontours)
    isCenter,center = findContourCenter([Maxcontour])



    if isCenter==True and isContour==True:
        center = center[0]
        cv2.drawContours(frame, Maxcontour[:], -1, (0,0,0), -1)
        cv2.circle(frame,center,3,(0,0,255),-1)
        dif = [(frameCenter[0]-center[0]),frameCenter[1]-center[1]]
        dif = [dif[0]/(frameCenter[0]/20),dif[1]/(frameCenter[1]/20)]
        minusH,minusV = Robot.turnRate(dif,coffH=1.7,ThresholdH=8,coffHAfter=1.2)
        if angle[1]>=4096:
            pass
        else:
            angle[1] -= minusH
        if angle[0]>=4096:
            pass
        else:
            angle[0] -= minusV
        if frameCenter[0]+50>center[0]>frameCenter[0]-50 and frameCenter[1]+50 > center[1] > frameCenter[1]-50:
            Robot.movemotor(42,angle[1],1023)
            Robot.movemotor(41,angle[0],1023)
            radAngel = (Robot.changeValueToRAD(angle[0]),Robot.changeValueToRAD(angle[1]))
            print 'rad',radAngel,'  ',angle
            distance = findDisFromPixel(frame.shape,center,FOV,33.0,offsetH=radAngel[1],offsetV=radAngel[0])
            text = "Her = {:.2f} Ver = {:.2f}".format(distance[0],distance[1])
            cv2.putText(frame,text,center,cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)
        else:
            Robot.movemotor(42,angle[1],1023)
            Robot.movemotor(41,angle[0],1023)


    # retGoal, listCnt, maskGoal, contours = TrackBall.getMaskAndCnt(frame, lower, upper,dst=notMaskGreen, trackShape=False)
    #
    # if retGoal == True:
    #     goalStat,GoalPos = TrackBall.goal(frame,listCnt,maskGoal)
    #     radAngel = (Robot.changeValueToRAD(angle[0]), Robot.changeValueToRAD(angle[1]))
    #     distance = findDisFromPixel(frame.shape, GoalPos, FOV, 33.0, offsetH=radAngel[1], offsetV=radAngel[0])
    #     cv2.putText(frame, goalStat, (0, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    #     cv2.putText(frame, str(distance), (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    #     cv2.circle(frame, GoalPos, 5, (0, 0, 0), -1)
    cv2.imshow('frame', frame)
    # cv2.imshow('mask',maskGoal)
    cv2.imshow('not',notMaskGreen)
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('p'):
        cv2.waitKey(0)
    end = time.time()
    print start-end


Robot.distorqAll()
cv2.destroyAllWindows()