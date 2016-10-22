import math
import time
from RobotControl import RobotControl

def Inverse3axis(X,Y,Z,h,l1,l2):
    x = X
    y = Y
    z = Z - h

    r = math.hypot(y,z)
    pho = math.hypot(r,x)
    phi = math.atan2(y, z)
    # xPrime = r
    # zPrime = -z
    xPrime = x
    zPrime = r

    cosTheta2 = ((xPrime*xPrime)+(zPrime*zPrime)-(l1*l1)-(l2*l2))/(2*l1*l2)
    sinTheta2 = math.sqrt(1-pow(cosTheta2,2))

    theta2 = math.atan2(sinTheta2 , cosTheta2)
    theta1 = math.atan2(zPrime,xPrime) - math.atan2(l2*sinTheta2,l1 + l2*cosTheta2)
    theta3 = math.atan2(y,z)
    # theta3 = phi

    return theta1,theta2,theta3

def calAngleForLeg(X,Y,Z,h=270,l1=135,l2=135):
    theta = Inverse3axis(X,Y,Z,h,l1,l2)
    print math.degrees(theta[0]),math.degrees(theta[1]),math.degrees(theta[2])

    theta1Robot = -((math.pi/2)-theta[0])
    theta2Robot = theta[1]
    theta3Robot = (math.pi - theta[2])

    theta4Robot = -( - math.fabs(theta2Robot) - theta1Robot)
    theta5Robot = theta3Robot

    return theta1Robot,theta2Robot,theta3Robot,theta4Robot,theta5Robot

def change(iterable,Robot):
    container = []
    for i in iterable:
        value = 2048-Robot.changeRad2Value(i)
        print 'value',value
        container.append(int(value))

    return container

def plusVec(iteration1,iteration2,mul1 = 1,mul2=1):
    list = []
    for i in range(0, len(iteration1)):
        list.append(iteration1[i]*mul1+ iteration2[i]*mul2)
    return list

print calAngleForLeg(0,0,135)

##############################################################################
vector = (85.0,85.0,100.0)
length = math.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)

unitVector = (vector[0]/length,vector[1]/length,vector[2]/length)
##############################################################################


angle = calAngleForLeg(85.0,85.0,100.0,h=305)



dic = {0:3,1:4,2:2,3:5,4:6}
Robot = RobotControl('COM5')
Robot.goCenter()
time.sleep(2)

pos = change(angle,Robot)


useTime = 4

print dic[1]
posNow = []

## read some value
Robot.get(1)
for i in range(0,5):
    a = Robot.get(dic[i])
    print a
    posNow.append(a)
begin = time.time()
now = time.time()

print pos
print posNow
while now<begin+useTime:

    p = posNow[0]+int(((pos[0]-posNow[0])*(now-begin))/(useTime))
    Robot.movemotor(3, p, 1023)
    p = posNow[1] + int(((pos[1] - posNow[1]) * (now - begin)) / (useTime))
    Robot.movemotor(4, p, 1023)
    p = posNow[2] + int(((pos[2] - posNow[2]) * (now - begin)) / (useTime))
    Robot.movemotor(2, p, 1023)
    p = posNow[3] + int(((pos[3] - posNow[3]) * (now - begin)) / (useTime))
    Robot.movemotor(5, p, 1023)
    p = posNow[4] + int(((pos[4] - posNow[4]) * (now - begin)) / (useTime))
    Robot.movemotor(6, p, 1023)
    # Robot.action()
    time.sleep(0.001)
    now = time.time()

Robot.movemotor(3,pos[0],500)
Robot.movemotor(4,pos[1],500)
Robot.movemotor(2,pos[2],500)
Robot.movemotor(5,pos[3],500)
Robot.movemotor(6,pos[4],500)
time.sleep(1)

posNow = []
## read some value
Robot.get(1)
for i in range(0,5):
    a = Robot.get(dic[i])
    print "Motor" + str(dic[i]) + " value = " + str(a)
    posNow.append(a)
begin = time.time()
now = time.time()

while now<begin+useTime:

    p = posNow[0]+int(((2048-posNow[0])*(now-begin))/(useTime))
    Robot.movemotor(3, p, 1023)
    p = posNow[1] + int(((2048 - posNow[1]) * (now - begin)) / (useTime))
    Robot.movemotor(4, p, 1023)
    p = posNow[2] + int(((2048 - posNow[2]) * (now - begin)) / (useTime))
    Robot.movemotor(2, p, 1023)
    p = posNow[3] + int(((2048 - posNow[3]) * (now - begin)) / (useTime))
    Robot.movemotor(5, p, 1023)
    p = posNow[4] + int(((2048 - posNow[4]) * (now - begin)) / (useTime))
    Robot.movemotor(6, p, 1023)
    # Robot.action()
    time.sleep(0.001)
    now = time.time()

Robot.movemotor(3,2048,1023)
Robot.movemotor(4,2048,1023)
Robot.movemotor(2,2048,1023)
Robot.movemotor(5,2048,1023)
Robot.movemotor(6,2048,1023)
time.sleep(1)

angle = calAngleForLeg(25.0,45.0,110.0,h=305)
pos = change(angle,Robot)

useTime = 4

posNow = []
## read some value
Robot.get(1)
for i in range(0,5):
    a = Robot.get(dic[i])
    print "Motor" + str(dic[i]) + " value = " + str(a)
    posNow.append(a)
begin = time.time()
now = time.time()
while now<begin+useTime:

    p = posNow[0]+int(((pos[0]-posNow[0])*(now-begin))/(useTime))
    Robot.movemotor(3, p, 1023)
    p = posNow[1] + int(((pos[1] - posNow[1]) * (now - begin)) / (useTime))
    Robot.movemotor(4, p, 1023)
    p = posNow[2] + int(((pos[2] - posNow[2]) * (now - begin)) / (useTime))
    Robot.movemotor(2, p, 1023)
    p = posNow[3] + int(((pos[3] - posNow[3]) * (now - begin)) / (useTime))
    Robot.movemotor(5, p, 1023)
    p = posNow[4] + int(((pos[4] - posNow[4]) * (now - begin)) / (useTime))
    Robot.movemotor(6, p, 1023)
    time.sleep(0.001)
    now = time.time()

Robot.movemotor(3,pos[0],500)
Robot.movemotor(4,pos[1],500)
Robot.movemotor(2,pos[2],500)
Robot.movemotor(5,pos[3],500)
Robot.movemotor(6,pos[4],500)
time.sleep(1)


posNow = []
## read some value
Robot.get(1)
for i in range(0,5):
    a = Robot.get(dic[i])
    print "Motor" + str(dic[i]) + " value = " + str(a)
    posNow.append(a)
begin = time.time()
now = time.time()

while now<begin+useTime:

    p = posNow[0]+int(((2048-posNow[0])*(now-begin))/(useTime))
    Robot.movemotor(3, p, 1023)
    p = posNow[1] + int(((2048 - posNow[1]) * (now - begin)) / (useTime))
    Robot.movemotor(4, p, 1023)
    p = posNow[2] + int(((2048 - posNow[2]) * (now - begin)) / (useTime))
    Robot.movemotor(2, p, 1023)
    p = posNow[3] + int(((2048 - posNow[3]) * (now - begin)) / (useTime))
    Robot.movemotor(5, p, 1023)
    p = posNow[4] + int(((2048 - posNow[4]) * (now - begin)) / (useTime))
    Robot.movemotor(6, p, 1023)
    # Robot.action()
    time.sleep(0.01)
    now = time.time()

Robot.movemotor(3,2048,1023)
Robot.movemotor(4,2048,1023)
Robot.movemotor(2,2048,1023)
Robot.movemotor(5,2048,1023)
Robot.movemotor(6,2048,1023)
Robot.action()