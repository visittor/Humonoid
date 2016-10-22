import cv2
import numpy as np
from countContours import *
from Vector import *
import math
import struct

class THRESHOLD_MASK():
    sample = []
    def __init__(self):
        self.frame = np.uint8

    def getFrame(self,frame):
        self.frame = frame
        Lowreso = cv2.pyrDown(self.frame)
        Lowreso = cv2.pyrDown(Lowreso)
        Lowreso = cv2.pyrDown(Lowreso)
        self.frameblur = cv2.pyrUp(Lowreso)
        self.frameblur = cv2.pyrUp(self.frameblur)
        self.frameblur = cv2.pyrUp(self.frameblur)

    def getCaribrate(self):
        hsv = cv2.cvtColor(self.frameblur,cv2.COLOR_BGR2HSV)
        self.sample.append(hsv[100,400])
        self.sample.append(hsv[250,400])
        self.sample.append(hsv[400,400])
        self.sample.append(hsv[100,445])
        self.sample.append(hsv[250,445])
        self.sample.append(hsv[400,445])
        self.sample.append(hsv[100,490])
        self.sample.append(hsv[250,490])
        self.sample.append(hsv[400,490])

        return self.sample

    def recieveSample(self,position,frame):
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        self.sample.append(hsv[position[1],position[0]])

    def popSample(self):
        self.sample.pop()

    def trackBegin(self):
        cv2.circle(self.frame,(400,100),5,(0,0,255),-1)
        cv2.circle(self.frame,(400,250),5,(0,0,255),-1)
        cv2.circle(self.frame,(400,400),5,(0,0,255),-1)
        cv2.circle(self.frame,(445,100),5,(0,0,255),-1)
        cv2.circle(self.frame,(445,250),5,(0,0,255),-1)
        cv2.circle(self.frame,(445,400),5,(0,0,255),-1)
        cv2.circle(self.frame,(490,100),5,(0,0,255),-1)
        cv2.circle(self.frame,(490,250),5,(0,0,255),-1)
        cv2.circle(self.frame,(490,400),5,(0,0,255),-1)


        """(400,100)(400,250)(445,)(490, """
    def createMask(self,sensitive):
        hsv = cv2.cvtColor(self.frameblur,cv2.COLOR_BGR2HSV)
        for i in range(0,len(self.sample)):
            maskTemp = cv2.inRange(hsv,np.array([self.sample[i][0]-sensitive,self.sample[i][1]-sensitive,self.sample[i][2]-sensitive]),np.array([self.sample[i][0]+sensitive,self.sample[i][1]+sensitive,self.sample[i][2]+sensitive]))
            if i == 0:
                mask = cv2.inRange(hsv,np.array([self.sample[i][0]-sensitive,self.sample[i][1]-sensitive,self.sample[i][2]-sensitive]),np.array([self.sample[i][0]+sensitive,self.sample[i][1]+sensitive,self.sample[i][2]+sensitive]))
            else:
                maskTemp = cv2.inRange(hsv,np.array([self.sample[i][0]-sensitive,self.sample[i][1]-sensitive,self.sample[i][2]-sensitive]),np.array([self.sample[i][0]+sensitive,self.sample[i][1]+sensitive,self.sample[i][2]+sensitive]))
                mask = cv2.bitwise_or(mask,maskTemp)
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.erode(mask,kernel,iterations = 1)
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.dilate(opening,kernel,iterations = 1)
        opening = cv2.GaussianBlur(opening,(17,17),0)
        return opening


class THRESHOLD_GRAY_MASK():
    sample = []
    def __init__(self):
        self.frame = np.uint8

    def getFrame(self,frame):
        self.frame = frame
        # cv2.imshow('frame',frame)

    def getCaribrate(self):
        pass

    def trackBegin(self):
        return
        print 'in'
    def createMask(self,sensitive):
        gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2LAB)
        Lowerb = np.array([0,0,103])
        Upperb = np.array([255,255,255])
        mask = cv2.inRange(gray,Lowerb,Upperb)
        kernel = np.ones((15,15),np.uint8)
        opening = cv2.erode(mask,kernel,iterations = 1)
        kernel = np.ones((7,7),np.uint8)
        opening = cv2.dilate(opening,kernel,iterations = 1)
        opening = cv2.GaussianBlur(opening,(17,17),0)
        cv2.imshow('mask',opening)
        return opening


class BACKPROJECTION_MASK:
    sample = []
    roihist1 = None
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    def __init__(self):
        self.frame = np.uint8

    def getFrame(self,frame):
        self.frame = frame
        self.mask1 = np.zeros(frame.shape[:2],np.uint8)
        self.mask1[133:183,327:377] = 255
        self.mask1[133:183,527:577] = 255
        self.mask1[333:383,327:377] = 255
        self.mask1[333:383,527:577] = 255
        self.hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    def getCaribrate(self):
        self.roihist1 = cv2.calcHist([self.hsv],[0, 1], self.mask1, [180/25, 256/25], [0, 180, 0, 256] )
        cv2.normalize(self.roihist1,self.roihist1,0,255,cv2.NORM_MINMAX)
        self.disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    def trackBegin(self):
        cv2.rectangle(self.frame,(327,133),(377,183),(0,0,255),4)
        cv2.rectangle(self.frame,(527,133),(577,183),(0,0,255),4)
        cv2.rectangle(self.frame,(327,333),(377,383),(0,0,255),4)
        cv2.rectangle(self.frame,(527,333),(577,383),(0,0,255),4)
    def createMask(self,sensitive):
        dst1 = cv2.calcBackProject([self.hsv],[0,1],self.roihist1,[0,180,0,256],1)
        cv2.filter2D(dst1,-1,self.disc,dst1)
        ret,thresh = cv2.threshold(dst1,100,255,0)
        kernel = np.ones((9,9),np.uint8)
        thresh = cv2.erode(thresh,kernel,iterations = 1)
        kernel = np.ones((11,11),np.uint8)
        thresh = cv2.dilate(thresh,kernel,iterations = 1)
        thresh = cv2.GaussianBlur(thresh,(17,17),0)
        return thresh

class createMask(THRESHOLD_GRAY_MASK,THRESHOLD_MASK,BACKPROJECTION_MASK):

    def __init__(self,method = THRESHOLD_GRAY_MASK):
        self.method = method
        self.method.__init__()

    def getFrame(self,frame):
        self.method.getFrame(frame)

    def getCaribrate(self):
        self.method.getCaribrate()

    def trackBegin(self):
        self.method.trackBegin()

    def createMask(self,sensitive):
        return self.method.createMask(sensitive)


def getContour(mask):
    _,contours,_ = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if len(contours)!=0:
        maxj = 0
        maxA = 0
        for j in range (len(contours)):
            cnt = contours[j]
            A = cv2.contourArea(cnt)
            if A>maxA:
                maxj = j
                maxA = A
                cnt = contours[maxj]

        return contours[maxj]
    else:
        return None

"""def drawPosition(frame,font,Outer,Inner,Points,circle):

    if Outer is not None:
        n = 1
        for i in Outer:
            cv2.circle(frame,i,4,(255,255,0),-1)
            cv2.putText(frame,str(n),i,font,1,(0,0,255))
            n += 1
        for j in Inner:
            cv2.circle(frame,j,4,(0,0,255),-1)
        for k in Points:
            cv2.circle(frame,k,8,(0,255,0),1)
    if circle is not  None:
        center = (int(circle.Center[0]),int(circle.Center[1]))
        cv2.circle(frame,center,int(circle.R),(0,0,255),3)
        cv2.circle(frame,center,int(circle.R*OUTER_RADIUS),(0,0,255),1)
        cv2.circle(frame,center,10,(0,100,255),-1)"""

def drawPosition(frame,circle,font,points=None,line = None):
    if points is not None:
        # print line
        for (key,value) in points.iteritems():
            n = 1
            if value is None:
                # print 'valuePoint',value
                pass
            else:
                for i in value:
                    cv2.circle(frame,i,4,key,-1)
                    cv2.putText(frame,str(n),i,font,1,(0,0,255))
                    n += 1
    if line is not None:
        for (key,value) in line.iteritems():
            if value[0] is None or value[1] is None:
                pass
            else:
                for (i,j) in zip(value[0],value[1]):
                    # print 'keyline',i,j
                    if i is None or j is None:
                        pass
                    else:
                        cv2.line(frame,i,j,key,2)
    if circle is not  None:
        center = (int(circle.Center[0]),int(circle.Center[1]))
        cv2.circle(frame,center,int(circle.R),(0,0,255),3)
        cv2.circle(frame,center,int(circle.R*OUTER_RADIUS),(0,0,255),1)
        cv2.circle(frame,center,10,(0,100,255),-1)
    return

def mssgHandle(mssg):
    header = struct.pack('L',len(mssg))
    body = mssg
    # print header+body
    return header+body

