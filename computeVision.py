import cv2
import numpy as np
from Vector import *


def findMaxAreaContour(contours):
    if len(contours) > 0:
        maxj = 0
        maxA = 0
        for j in range(len(contours)):
            cnt = contours[j]
            A = cv2.contourArea(cnt)
            if A > maxA:
                maxj = j
                maxA = A
                cnt = contours[maxj]

        return True,contours[maxj]
    else:
        return False,None
def findContourInShape(contours,percen,shape):
    dataApp = []
    dataCnt = []
    ret =False
    if contours is not None:
        for cnt in contours:
            elipson = percen * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, elipson, True)
            if shape[0]<len(approx)<shape[1]:
                dataApp.append(approx)
                dataCnt.append(cnt)
        if len(dataCnt)>0:
            ret = True
        return ret,dataCnt

def removeNoise(img,erode,dilation,blur):
    kernel = np.ones(erode, np.uint8)
    img = cv2.erode(img, kernel, iterations=1)
    kernel = np.ones(dilation, np.uint8)
    img = cv2.dilate(img, kernel, iterations=2)
    img = cv2.GaussianBlur(img, blur, 0)
    return img

def findContourCenter(Cnt,offsetX = 0,offsetY = 0):
    center = []
    for cnt in Cnt:
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            print 'in'
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center.append((cx+offsetX,cy+offsetY))
    if len(center)>0 :
        return True,center
    else:
        return False,None

def skeletonization(mask):
    size = mask.size
    kernel = np.ones((3,3), np.uint8)
    skeleton = np.zeros(mask.shape,np.uint8)
    while True:
        erode = cv2.erode(mask,kernel)
        dila = cv2.dilate(erode,kernel)
        sub = cv2.subtract(mask,dila)
        skeleton = cv2.bitwise_or(sub,skeleton)
        mask = erode.copy()
        # cv2.imshow('skelPre', skeleton)
        # cv2.imshow('mask',mask)
        # cv2.imshow('sub',sub)
        # cv2.waitKey(100)
        zeros = size - cv2.countNonZero(mask)
        if zeros == size:
            break
    # cv2.imshow('skel',skeleton)
    # cv2.waitKey(1)
    # skeleton = cv2.Canny(skeleton, 50,100)
    return skeleton

class Track(Vector):

    def __init__(self,erode_=(1,1),dilation_=(1,1),blur_=(0,0),shape_ = None,colorSpace = cv2.COLOR_BGR2HSV):
        self.erode = erode_
        self.dilation = dilation_
        self.blur = blur_
        self.shape = shape_
        self.colocode = colorSpace

    def getOnlyMask(self,img,lower,upper,removenoise = True):
        lab = cv2.cvtColor(img,self.colocode)
        mask = cv2.inRange(lab,lower,upper)
        if removenoise:
            mask = removeNoise(mask,self.erode,self.dilation,self.blur)
        return mask

    def getMaskAndCnt(self,img,lower,upper,percen = 0.03,dst = None, mask = None , trackShape = True):
        if mask is None:
            lab = cv2.cvtColor(img,self.colocode)
            mask = cv2.inRange(lab,lower,upper)
            mask = removeNoise(mask,self.erode,self.dilation,self.blur)
        if dst is not None:
            # _,dstCnt,_ = cv2.findContours(dst.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # _,dstMax = findMaxAreaContour(dstCnt)
            # cv2.drawContours(img,dstMax,-1,255,2)
            mask = cv2.bitwise_and(mask.copy(),dst)
        if self.shape is not None and trackShape == True:
            try:
                _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                ret,listCnt = findContourInShape(contours,percen,self.shape)
                return ret,listCnt,mask,contours
            except cv2.error:
                print 'mask  ',' ',mask,' ',type(mask),' ',len(mask)
                return False,[],mask,[]
        else:
            _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ret,listCnt = findMaxAreaContour(contours)
            return ret,listCnt,mask,contours

    def chooseOne(self,Cnt,Allcontours):
        if len(Cnt) == 0:
            ret,MaxContour = findMaxAreaContour(Allcontours)
        elif len(Cnt) > 1:
            ret,MaxContour = findMaxAreaContour(Cnt)
        else:
            print  'else'
            MaxContour = Cnt[0]
            ret = True
        if MaxContour is None:
            ret = False
        return ret,MaxContour

    def goal(self,frame,cnt,mask):
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3)
        topLeft = mask[y:y+h/2,x:x+w/2]
        topRight = mask[y:y+h/2,x+w/2:x+w]
        botLeft = mask[y+h/2:y+h,x:x+w/2]
        botRight = mask[y+h/2:y+h,x+w/2:x+w]
        topLeftRet,_, _,_ = self.getMaskAndCnt(topLeft, None, None,mask=topLeft)
        topRightRet, _, _, _ = self.getMaskAndCnt(topRight, None, None, mask=topRight)
        botLeftRet, _, _, _ = self.getMaskAndCnt(botLeft, None, None, mask=botLeft)
        botRightRet, _, _, _ = self.getMaskAndCnt(botRight, None, None, mask=botRight)

        bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

        area = cv2.contourArea(cnt)
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        if hull_area == 0:
            cv2.waitKey(0)
            return '...'
        solidity = float(area) / hull_area

        if topLeftRet and topRightRet and botRightRet and botLeftRet and solidity<0.85:
            return 'Goal',bottommost

        # elif topLeftRet and topRightRet:
        #     return 'Whole Goal'

        elif topLeftRet and topRightRet and botRightRet and botLeftRet == False and solidity<0.85:
            return 'Right',bottommost

        elif topLeftRet and topRightRet and botLeftRet and botRightRet == False and solidity<0.85:
            return 'Left',bottommost

        else:
            return 'Unknow',bottommost

    def __lineAnalyse(self,lines):
        vector = Vector()
        if  lines is None:
            return 'Unknow',None,None,None
        if len(lines)==0:
            return  'Unknow',None,None,None

        x0,y0,x1,y1 = lines[0][0]
        pivot0 = (x0,y0)
        pivot1 = (x1,y1)
        pivotVec = vector.creatVector(pivot0,pivot1)
        np.delete(lines,0)
        normalPiv = pivotVec.normalize()
        refVec = None

        dotMin = np.inf

        for line in lines:
            x0,y0,x1,y1 = line[0]
            temp0 = (x0,y0)
            temp1 = (x1,y1)
            tempVec = vector.creatVector(temp0,temp1)
            dot =vector.dotproduct(normalPiv,tempVec.normalize())
            print 'dot',dot, normalPiv.length
            if  dot**2 < dotMin**2 and dot<0.12:
                dotMin = dot
                refVec = tempVec

        # print 'dotMin', dotMin, normalPiv.length
        if refVec is None:
            return 'Unknow',None,None,None

        normalRef = refVec.normalize()

        lineRef = vector.line(refVec.point1,refVec.point2)
        linePivot = vector.line(pivotVec.point1,pivotVec.point2)

        point = vector.intersect(lineRef,linePivot)

        reference = zip(refVec.point1,refVec.point2)
        pivot = zip(pivotVec.point1,pivotVec.point2)

        for line in lines:
            x0, y0, x1, y1 = line[0]
            temp0 = (x0, y0)
            temp1 = (x1, y1)
            temp = zip(temp0,temp1)
            tempVec = vector.creatVector(temp0, temp1)
            tempVec = tempVec.normalize()
            if vector.dotproduct(tempVec,normalRef)>0.9 and (max(temp[0])<min(reference[0])-20 or min(temp[0])>max(temp[0])+20):
                return 'T',point,lineRef,linePivot

            if vector.dotproduct(tempVec,normalPiv)>0.9 and (max(temp[0])<min(pivot[0])-20 or min(temp[0])>max(pivot[0])+20):
                return 'T',point,lineRef,linePivot
        return 'L',point,lineRef,linePivot

    def Line(self,mask):
        skel = skeletonization(mask.copy())

        kernel = np.ones((3, 3), np.uint8)
        skel = cv2.dilate(skel, kernel, iterations=2)
        skel = cv2.erode(skel, kernel, iterations=2)

        lines = cv2.HoughLinesP(skel, 1, np.pi / 720, 150, minLineLength=50, maxLineGap=10)
        status,point,lineRef,linePivot = self.__lineAnalyse(lines)
        # p2 = lineRef.startPoint+lineRef.vector*1000
        # cv2.line(mask,(int(lineRef.startPoint.point1[0]),int(lineRef.startPoint.point1[1])),(int(p2.point1[0]),int(p2.point1[1])),0,5)
        # p2 = linePivot.startPoint + linePivot.vector * 1000
        # cv2.line(mask, (int(linePivot.startPoint.point1[0]), int(linePivot.startPoint.point1[1])),(int(p2.point1[0]), int(p2.point1[1])), 0, 5)
        # (int(lineRef.startPoint.point1[0] + lineRef.vector.x * 10)), int(lineRef.startPoint.point1[1] + lineRef.vector.y * 10))
        if point is not None:
            # cv2.circle(mask,(point.x,point.y),4,0,-1)
            print dir(point)
        return status,lines,point


if __name__ == '__main__':
    while True:
        img = cv2.imread('hand.png',0)
        skeletonization(img)
        # cv2.destroyAllWindows()
        cv2.waitKey(1)

