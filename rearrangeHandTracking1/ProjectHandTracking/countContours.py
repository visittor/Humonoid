import numpy as np
import cv2
from Vector import *

OUTER_RADIUS = 1.75
HIGH_THRESHOLD = 30
ANGLE_THRESHOLD = -0.85
SKIPPING_INDEX = 25
INDX_THRESHOLD_FING = 75
INDX_THRESHOLD_INTERSECT = 20
FIND_INNER_VECTOR_LENGTH_MULTIPLIER = 0.2
HAND_CENTER_PIXEL_SENTSITIVE = 5

def countContours(contour,shape,mask,RetIndx = False):
    Intemp = -9999
    Points = []
    testPoints = []
    Inner = []
    Outer = []
    onCircle = []
    references = []
    wrist = []
    Vectorcal = Vector()
    circleCal = circleCalculator()
    if contour is None :
        return (None,None,None)
    center,raduis = findMaxIncribedCircle(contour,shape)
    circle = circleCal.circleCreate(center,raduis)
    onCircle,listIndx = InDahCircle(circle,contour)
    references,wrist,listIndx = identifyRef(onCircle,contour,listIndx)
    for i in listIndx:
        testPoints.append((contour[i][0][0],contour[i][0][1]))
    for Indx in range(0,len(contour),SKIPPING_INDEX):
        cosAngle = findAngleInContour(contour,Indx,Vectorcal)
        # cosAngleForward = findAngleInContour(contour,Indx+SKIPPING_INDEX,Vectorcal)
        # cosAngleBackward = findAngleInContour(contour,Indx-SKIPPING_INDEX,Vectorcal)
        if cosAngle >= ANGLE_THRESHOLD:
        # if cosAngle >= cosAngleBackward and cosAngle>=cosAngleForward:
            if contour[Indx][0][0] >= shape[1]-10 or contour[Indx][0][1] >= shape[0]-10:
                pass
            if Intemp> Indx-INDX_THRESHOLD_FING and len(Points)>0 :
                print 'eiei'
                cosAngleTemp = findAngleInContour(contour,Intemp,Vectorcal)
                if cosAngleTemp>cosAngle:
                    pass
                else:
                    Points.pop(-1)
                    Points.append((contour[Indx][0][0],contour[Indx][0][1]))
                    Intemp = Indx
            else:
                Points.append((contour[Indx][0][0],contour[Indx][0][1]))
                Intemp = Indx

    if len(Points)>1:
        pointEnd = Points[-1]
        pointStart = Points[0]
        if Vectorcal.findLenght(pointEnd,pointStart)< 0.1*cv2.arcLength(contour,True):
            Points.pop(-1)
            Points[0] = ((pointStart[0]+pointEnd[0])/2,(pointStart[1]+pointEnd[1])/2)
            pass

    for ptsIndx in range(0,len(Points)):
        lenght = Vectorcal.findLenght(Points[ptsIndx],circle.Center)
        if ptsIndx == 0 or ptsIndx == len(Points)-1:
            if Points[ptsIndx][0]>=shape[1]-HIGH_THRESHOLD or Points[ptsIndx][1] >= shape[0]-HIGH_THRESHOLD:
                pass
            elif lenght<=circle.R*OUTER_RADIUS:
                Inner.append(Points[ptsIndx])
            elif findInner(Points[(ptsIndx-1)%len(Points)],Points[ptsIndx],Points[(ptsIndx+1)%len(Points)],mask):
                Inner.append(Points[ptsIndx])
            else:
                Outer.append(Points[ptsIndx])
        else:
            if Points[ptsIndx][0]>=shape[1]-HIGH_THRESHOLD or Points[ptsIndx][1] >= shape[0]-HIGH_THRESHOLD:
                pass
            elif lenght<=circle.R*OUTER_RADIUS:
                Inner.append(Points[ptsIndx])
            elif findInner(Points[(ptsIndx-1)],Points[ptsIndx],Points[(ptsIndx+1)],mask):
                Inner.append(Points[ptsIndx])
            else:
                Outer.append(Points[ptsIndx])
        if len(references) == len(Outer):
            return (testPoints,Inner,Points,circle,onCircle,references,wrist)
    return (Outer,Inner,Points,circle,onCircle,None,None)

def findAngleInContour(contour,Indx,Vectorcal):
    point1 = contour[(Indx-SKIPPING_INDEX)%len(contour)][0]
    point2 = contour[(Indx)%len(contour)][0]
    point3 = contour[(Indx+SKIPPING_INDEX)%len(contour)][0]
    cosAngle = Vectorcal.findAngle(point1,point2,point3)
    return cosAngle

def findInner(pt1,pt2,pt3,mask):
    h,w = mask.shape
    Vectorcal = Vector()
    vec1 = Vectorcal.creatVector(pt2,pt1)
    vec2 = Vectorcal.creatVector(pt2,pt3)
    (x1,y1) = (pt2[0]+(FIND_INNER_VECTOR_LENGTH_MULTIPLIER*vec1.x),pt2[1]+(FIND_INNER_VECTOR_LENGTH_MULTIPLIER*vec1.y))
    (x2,y2) = (pt2[0]+(FIND_INNER_VECTOR_LENGTH_MULTIPLIER*vec2.x),pt2[1]+(FIND_INNER_VECTOR_LENGTH_MULTIPLIER*vec2.y))
    if y1>=h or y2>=h or x1>=w or x2>=w or y1<=0 or y2<=0 or x1<=0 or x2<=0:
        return False
    elif mask[y1][x1] == 0 and mask[y2][x2] == 0:
        return False
    else:
        return True

def identifyRef(points,cnt,listIndx):
    if points ==0:
        return [],[]
    ref = []
    wrist = []
    vectorCal = Vector()
    maxI = 0
    maxLenght = 0
    n = 0
    Indx2return = []
    for i in range(-1,len(points)-1,2):
        p1 = points[i]
        p2 = points[(i+1)%len(points)]
        Indx1 =listIndx[(i)]-int(len(cnt)*(listIndx[(i)]/(len(cnt)/2)))
        Indx2 = listIndx[(i+1)%len(points)]-int(len(cnt)*(listIndx[(i+1)%len(points)]/(len(cnt)/2)))
        P = ((p1[0]+p2[0])/2,(p2[1]+p1[1])/2)
        Indx = int(((Indx2+Indx1)/2))
        if cv2.pointPolygonTest(cnt,P,False) == 1:
            ref.append(P)
            Indx2return.append(Indx)
            lenght = vectorCal.findLenght(p1,p2)
            if lenght>maxLenght:
                maxI = n
                maxLenght = lenght
            n += 1
    wrist=ref[maxI]
    ref.pop(maxI)
    Indx2return.pop(maxI)
    return ref,wrist,Indx2return

def AnalysisPoints(Outer,Inner,Points,contour,shape):
    VectorCal = Vector()
    cirCal = circleCalculator()
    center,radius = findMaxIncribedCircle(contour,shape)
    circle = cirCal.circleCreate(center,radius)
    if circle is not None:
        inner = []
        inner.extend(Inner)
        outIndx = 0
        while outIndx<len(Outer):
            lenght = VectorCal.findLenght(Outer[outIndx],circle.Center)
            if lenght<OUTER_RADIUS*circle.R:
                Outer.pop(outIndx)
            else:
                outIndx += 1
    elif circle is None:
        return (None,None,None,None,None)

    data = []
    data.append(circle.Center)
    data.extend(Outer)
    data.append(len(Outer))
    return (data,Outer,Inner,Points,circle)

def findMaxIncribedCircle(contour,shape):
    if contour is not None:
        epsilon = 0.02*cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,epsilon,True)
        x,y,w,h = cv2.boundingRect(contour)
        dist = np.zeros((shape[0],shape[1]),dtype=np.uint8)
        for xAxis in range(x,x+w,HAND_CENTER_PIXEL_SENTSITIVE):
            for yAxis in range(y,y+h,HAND_CENTER_PIXEL_SENTSITIVE):
                D = cv2.pointPolygonTest(approx,(xAxis,yAxis),True)
                if D > 0 :
                    dist[yAxis,xAxis] = D
                else:
                    dist[yAxis,xAxis] = 0
        minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(dist)
        return (maxLoc,maxVal)
    elif contour is None:
        return (None,None)

def InDahCircle(circle,Points):
    vectorCal = Vector()
    list = []
    listIndx = []
    IndxTemp = 0
    for Indx in range(0,len(Points),2):
        if circle.R*OUTER_RADIUS+2>=vectorCal.findLenght(Points[Indx][0],circle.Center) >= circle.R*OUTER_RADIUS-2:
            if Indx>IndxTemp+INDX_THRESHOLD_INTERSECT:
                list.append((Points[Indx][0][0],Points[Indx][0][1]))
                listIndx.append(Indx)
                IndxTemp = Indx
            else:
                if vectorCal.findLenght(Points[Indx][0],circle.Center)<=vectorCal.findLenght(Points[IndxTemp][0],circle.Center):
                    pass


    return list,listIndx

