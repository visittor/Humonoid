import cv2
import numpy as np
import math
#comment
def findFieldOfView(Xver,Yver,Xher,Yher):
    tanVer = float(Yver)/float(Xver)
    tanHer = float(Yher)/float(Xher)
    FOV = np.arctan([tanHer,tanVer])
    FOV[0]=FOV[0]*2
    FOV[1] = FOV[1]*2
    return FOV

def findDisFromPixel(shape,pixel,FOV,Height,offsetH = 0,offsetV = 0):
    fov = [FOV[0]/2,FOV[1]/2]
    centerFrame = (shape[1]/2,shape[0]/2)
    angleV = float(fov[1] * (float(centerFrame[1] - pixel[1]) / float(centerFrame[1])))+offsetV
    # angleV = (fov[1]*(pixel[1]-centerFrame[0])/centerFrame[0])+offsetV
    angleH = float(fov[0] * (pixel[0] - centerFrame[0])) / float(centerFrame[0])+offsetH
    # angleH = (fov[0]*(pixel[0]-centerFrame[1])/centerFrame[1])+offsetH
    # print 'angleV=',angleV,'angleH=',angleH
    disV = float(Height)/np.tan([angleV])[0]
    disH = float(disV)*np.tan([angleH])[0]
    return disH,disV