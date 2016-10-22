import cv2
import numpy as np
from computeVision import *
import time
import imutils
import glob

imagePath = sorted(glob.glob('tesPic/*.jpg'))
print imagePath
# cap = cv2.VideoCapture(1)
erode = (7,7)
dilation = (7,7)
blur = (15,15)
lowerGreen = np.array([0,0,0])
upperGreen = np.array([203,105,172])
lowerWhite = np.array([165,115,115])
upperWhite = np.array([255,255,255])
TrackBall = Track(erode_=erode,dilation_=dilation,blur_=blur,shape_=(1,10),colorSpace=cv2.COLOR_BGR2LAB)
index4path = 0
while True:
    start = time.time()
    frame = cv2.imread(imagePath[index4path%len(imagePath)])
    frameCenter = (frame.shape[1]/2,frame.shape[0]/2)
    frame = cv2.flip(frame, 0)

    maskGreen = TrackBall.getOnlyMask(frame, lowerGreen, upperGreen,removenoise=True)
    _, c, _ = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ret, cntWhite, maskWhite, allContoursWhite = TrackBall.getMaskAndCnt(frame, lowerWhite, upperWhite, percen=0.035, dst=None)

    status,lines,point = TrackBall.Line(maskWhite)
    cv2.putText(frame, status, (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    # print (int(point.point1[0]),int(point.point1[1]))
    if point is not None:
        cv2.circle(frame,(int(point.point1[0]),int(point.point1[1])),50,[0,0,255],-1)

    skeletonWhite = skeletonization(maskWhite.copy())
    kernel = np.ones((3, 3), np.uint8)
    skeletonWhite = cv2.dilate(skeletonWhite, kernel, iterations=2)
    skeletonWhite = cv2.erode(skeletonWhite, kernel, iterations=1)
    corner = cv2.goodFeaturesToTrack(maskWhite,50,0.2,10)

    for i in corner:
        x = i[0][0]
        y = i[0][1]
        cv2.circle(frame, (x, y), 3, 255, -1)

    # if lines is not None:
    #     print len(lines)
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    stack = np.hstack((maskWhite,skeletonWhite))
    cv2.imshow('skel',stack)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(0)
    index4path += 1
    print index4path
    if k ==27:
        break

cv2.destroyAllWindows()
