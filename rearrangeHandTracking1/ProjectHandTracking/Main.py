from Vector import *
from countContours import *
from classForJimmy import *
import cv2
import numpy as np
import argparse
import socket
import json
import pickle

ap = argparse.ArgumentParser()
ap.add_argument("-i","--id",type = str,default='0',help="camera id")
ap.add_argument("-m","--method",default="THRESHOLD_MASK",help="Method which used to creat mask")
ap.add_argument("-c","--capture",type=bool,default=False,help="Method which used to creat mask")
args = vars(ap.parse_args())

dict = {"THRESHOLD_GRAY_MASK":THRESHOLD_GRAY_MASK(),"THRESHOLD_MASK":THRESHOLD_MASK(),"BACKPROJECTION_MASK":BACKPROJECTION_MASK()}
if args["id"].isdigit():    CAMERA_ID = int(args["id"])
else: CAMERA_ID = args["id"]
MASK_METHOD = dict[args["method"]]
MASK_SENSITIVE = 25

# s = socket.socket()
# host = socket.gethostbyname(socket.gethostname())
# print host
# port = 1506
# s.bind((host,port))
# s.listen(5)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
if args["capture"]==True:
    out = cv2.VideoWriter('Hand.avi',fourcc,13.0,(640,480))
click = False
caribrate = 0
font = cv2.FONT_HERSHEY_COMPLEX


def set(event,x,y,flag,param):
    global click
    if flag == cv2.EVENT_LBUTTONDOWN:
        # print x,y
        click = True
        return (x,y)
cv2.namedWindow('window')
cv2.setMouseCallback('window',set)
maskCreator = createMask(method=MASK_METHOD)
cap = cv2.VideoCapture(CAMERA_ID)

# c,adr = s.accept()
# print 'got',adr
circle = None

while True:
    ret,frame = cap.read()
    mask = np.zeros(frame.shape)
    maskCreator.getFrame(frame)
    # request = c.recv(4096)
    # print request,'\n'
    if click == True and caribrate <2:
        maskCreator.getCaribrate()
        caribrate += 1
        print caribrate
        click = False
        # c.send('recieve')

    elif caribrate >= 2:
        mask = maskCreator.createMask(MASK_SENSITIVE)
        contour = getContour(mask)
        cv2.drawContours(frame, [contour], -1, (255,255,255), 2)
        Outer,Inner,Points,circle,onCircle,reference,wrist = countContours(contour,frame.shape,mask)
        data,Outer,Inner,Points,circle = AnalysisPoints(Outer,Inner,Points,contour,mask.shape)
        # if request == 'request':
        #     c.send('begin')
        #     if circle is not None:
        #         mssg = pickle.dumps((data,Outer,Inner,circle.Center,circle.R,))
        #     else:
        #         mssg = pickle.dumps((None,None,None,None,None,None))
        #     mssg2send = mssgHandle(mssg)
        #     c.send(mssg)
        # else:
        #     c.send('recieve')
        # print 'Points',Points
        list2draw = {(255,0,0):Outer,(0,255,0):reference,(0,0,255):[wrist],(0,255,255):onCircle}
        point4line = {(255,0,255):(Outer,reference),(0,255,255):([circle.Center],[wrist])}
        drawPosition(frame,circle,font,points=list2draw,line=point4line)

    else:
        maskCreator.trackBegin()
        # c.send('recieve')
    cv2.imshow('window',frame)
    if args["capture"]==True: out.write(frame)
    k = cv2.waitKey(20)
    if k == 27:
        break
    elif k == ord('p'):
        cv2.waitKey(0)
if args["capture"]==True: out.release()
cap.release()
cv2.destroyAllWindows()