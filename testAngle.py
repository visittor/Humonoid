import cv2
import numpy as np
from Camera import *
from RobotControl import *

cap = cv2.VideoCapture(1)

fov = findFieldOfView(60,28,102.5,60)
FOV = fov
fov = [fov[0]/2,fov[1]/2]
print fov[0],',',fov[1]

Robot = RobotControl('COM5')
Robot.movemotor(42,2046,1023)
Robot.movemotor(41,2046,1023)
cv2.waitKey(1500)
angle = Robot.get(41)
cv2.waitKey(1500)
angleOffset = Robot.changeValueToRAD(angle)

print angleOffset

while True:
    isOpen,frame = cap.read()
    frame = cv2.flip(frame, 0)
    shape = frame.shape
    centerFrame = (shape[1]/2,shape[0]/2)
    # print 'centerFrame',centerFrame
    # print 'shape',shape
    '''Herizontal'''
    for i in range(0,shape[1],40):
        cv2.line(frame,(i,0),(i,shape[0]),(255,255,255),1)
        angleH = float(fov[0] * (i - centerFrame[0])) / float(centerFrame[0])
        disH,_ = findDisFromPixel(shape,(i,460),FOV,30.0,offsetV=angleOffset)
        # angleV = 360*angleV/(2*np.pi)
        text = '{:.1f}'.format(disH/1)
        text2 = '{:.1f}'.format(angleH+angleOffset)
        cv2.putText(frame,text,(i, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255,160), 1)
        cv2.putText(frame, text2, (i, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255,160), 1)
    '''Vertical'''
    for i in range(0, shape[0], 20):
        cv2.line(frame, ( 0,i), (shape[1],i), (255, 255, 255), 1)
        angleV = float(fov[1] * (float(centerFrame[1]-i) / float(centerFrame[1])))
        _, disV = findDisFromPixel(shape, (0, i), FOV, 30.0,offsetV=angleOffset)
        # angleV = 360*angleV/(2*np.pi)
        text = '{:.1f}'.format(disV)
        text2 = '{:.2f}'.format(angleV + angleOffset)
        cv2.putText(frame, text, (600,i), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        cv2.putText(frame, str(i), ( 40,i), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

    cv2.imshow('frame',frame)
    k = cv2.waitKey(10)
    if k == 27:
        break

# cap.releash()
cv2.destroyAllWindows()