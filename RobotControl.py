import serial
import time
import math
import numpy as np

class RobotControl():
    int_id_L = [1, 2, 3, 4, 5, 6]
    int_id_R = [11, 12, 13, 14, 15, 16]
    int_id_LArm = [21, 22, 23]
    int_id_RArm = [31, 32, 33]
    int_id_H = [41, 42]
    int_id_All = int_id_L + int_id_R + int_id_LArm + int_id_RArm + int_id_H


    def __init__(self,port,buerd=1000000,MaxValue = 4096,timeout = 0.1):
        self.MaxValue = MaxValue
        self.Port = port
        self.Buerd = buerd
        self.ser = serial.Serial(port)
        self.ser.baudrate = buerd
        self.timeout = timeout

################################### for control servo mortor ###################################
    def readData(self):
        packet = []
        startTime = time.clock()
        while time.clock() - startTime<=self.timeout:
            while self.ser.inWaiting():
                packet.append(ord(self.ser.read()))
        return packet

    def movemotor(self, id, angle, speed):
        angleL = angle % 256
        angleH = (angle - angleL) / 256
        speedL = speed % 256
        speedH = (speed - speedL) / 256
        x = [255, 255, id, 7, 3, 30, int(angleL), int(angleH), int(speedL), int(speedH)]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        self.ser.write(x)

    def movemotorWithoutSpeed(self, id, angle):
        angleL = angle % 256
        angleH = (angle - angleL) / 256
        x = [255, 255, id, 5, 3, 30, int(angleL), int(angleH)]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        print x
        self.ser.write(x)

    def REGmotor(self,id,angle,speed):
        angleL = int(angle)%256
        angleH = int(angle - angleL) / 256
        # print angleH,angleL
        speedL = speed % 256
        speedH = (speed - speedL) / 256
        x = [255, 255, id, 7, 4, 30, int(angleL), int(angleH), int(speedL), int(speedH)]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        self.ser.write(x)
        time.sleep(0.00075)

    def readangle(self, id):
        x = [255, 255, id, 4, 2, 36, 2]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        print 'read',a
        self.ser.write(x)

    def get(self, id):
        self.readangle(id)
        position = self.readData()
        data = position
        print "packet from id "+str(id)+" is ",data
        if len(data) > 6:
            angle = (data[-3]) + 256 * (data[-2])
            return angle

        time.sleep(0.0015)

    def distorq(self, id):
        x = [255, 255, id, 4, 3, 24, 0]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        self.ser.write(x)
        # print('Dis/En sent to', id)

    def distorqAll(self):
        for i in self.int_id_All:
            self.distorq(i)
        self.action()

    def REGdistorq(self, id):
        x = [255, 255, id, 4, 4, 24, 0]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        self.ser.write(x)
        print('Dis/En sent to', id)

    def action(self):
        self.ser.write([255, 255, 254, 2, 5, 250])

    def clicktorqall(self):
        for i in self.int_id_All:
            self.REGdistorq(i)
        self.action()

    def ping(self,id):
        x = [255,255,id,2,1]
        a = (~((sum(x) - 510) % 256)) % 256
        x.append(a)
        self.ser.write(x)
        time.sleep(0.04)

    def goCenter(self):
        for i in self.int_id_All:
            self.movemotor(i,self.MaxValue/2,1023)
        time.sleep(0.1)
################################################################################################

############################# about see a ball just ignore it ##################################
    def turnRate(self,dif,coffH = 1.5,coffV = 1.5,ThresholdH = 12,ThresholdV = 11,coffVAfter=1.1,coffHAfter = 1.1):
        if dif[0] == 0:
            minusH = 0
        else:
            minusH = ((coffH ** (math.fabs(dif[0])))) * (dif[0]) / math.fabs(dif[0])
            # minusH = 10*dif[0]
        if dif[1] == 0:
            minusV = 0
        else:
            minusV = ((coffV ** math.fabs(dif[1])) * (dif[1])) / math.fabs(dif[1])
        if dif[0] > ThresholdH or dif[0] < -ThresholdH:
            minusH = ((coffHAfter ** (math.fabs(dif[0]))) + math.fabs(coffH ** (math.fabs(ThresholdH)))) * (dif[0]) / math.fabs(dif[0])

        if dif[1] > ThresholdV or dif[1] < -ThresholdV:
            minusV = ((coffVAfter ** (math.fabs(dif[1]))) + math.fabs(coffV ** math.fabs(ThresholdV))) * (dif[1]) / math.fabs(dif[1])

        return minusH,minusV
################################################################################################

######################### change value to RAD or RAD t ovalue ##################################
    def changeValueToRAD(self,value):
        rad = np.pi - (1.3333*np.pi*(float(value)/float(self.MaxValue)))
        return rad

    def changeRad2Value(self,rad):
        if rad > np.pi:
            rad = rad - 2*np.pi

        elif rad < -np.pi:
            rad = rad + 2*np.pi
        value = (self.MaxValue*rad)/(1.33333*np.pi)
        return value
################################################################################################

#################################### Inverse kinametic #########################################
    def moveRobotLegFromAngleInRAD(self,angle,side = 'L'):
        container = []
        for i in range (0,len(angle)):
            if side == 'L':
                value = (self.MaxValue/2) - self.changeRad2Value(angle[i])
            elif side == 'R':
                if 4>i>0:
                    value = self.changeRad2Value(angle[i]) +(self.MaxValue/2)
                else:
                    value = (self.MaxValue/2) - self.changeRad2Value(angle[i])
            print 'value', value
            container.append(int(value))

        return container
#################################################################################################

    def controlSpeedMotor(self,useTime,list_motor_id,list_pos):
        current_pos = []
        Robot.get(1)
        for i in range(0, len(list_motor_id)):
            a = Robot.get(list_motor_id[i])
            print "Motor" + str(list_motor_id[i]) + " value = " + str(a)
            current_pos.append(a)

        begin = time.time()
        now = time.time()
        while now < begin + useTime:
            for i in range(0,len(list_motor_id)):
                p = current_pos[i] + int(((list_pos[i] - current_pos[i]) * (now - begin)) / (useTime))
                self.movemotor(list_motor_id[i], p, 1023)
            now = time.time()
            time.sleep(0.00075)

        for i in range(0,len(list_motor_id)):
            self.movemotor(list_motor_id[i], list_pos[i], 1023)
            # time.sleep(0.0001)
        time.sleep(0.001)

class kinematicsCalculator():

    def __init__(self):
        pass

    def Inverse3axis(self, X, Y, Z, h, l1, l2):
        x = X
        y = Y
        z = Z - h

        r = math.hypot(y, z)
        xPrime = x
        zPrime = r

        cosTheta2 = ((xPrime * xPrime) + (zPrime * zPrime) - (l1 * l1) - (l2 * l2)) / (2 * l1 * l2)
        sinTheta2 = math.sqrt(1 - pow(cosTheta2, 2))

        theta2 = math.atan2(sinTheta2, cosTheta2)
        theta1 = math.atan2(zPrime, xPrime) - math.atan2(l2 * sinTheta2, l1 + l2 * cosTheta2)
        theta3 = math.atan2(y, z)

        return theta1, theta2, theta3

    def calAngleForLeg(self, X, Y, Z, h=270, l1=135, l2=135):
        theta = self.Inverse3axis(X, Y, Z, h, l1, l2)
        print math.degrees(theta[0]), math.degrees(theta[1]), math.degrees(theta[2])

        theta1Robot = -((math.pi / 2) - theta[0])
        theta2Robot = theta[1]
        theta3Robot = math.pi - theta[2]

        theta4Robot = -(- math.fabs(theta2Robot) - theta1Robot)
        theta5Robot = theta3Robot

        return theta3Robot, theta1Robot, theta2Robot, theta4Robot, theta5Robot




if __name__ == '__main__':
    x = [255, 255, 4 ,5 ,3 ,6 ,144 ,1]
    # x = [255, 255, 8, 4, 2, 36, 2]
    a = (~((sum(x) - 510) % 256)) % 256
    print 'check', a
    Robot = RobotControl('COM5')
    Robot.get(5)
    Robot.goCenter()
    time.sleep(1)
    # Robot.movemotorWithout(5,100,1023)
    # angle = Robot.get(5)
    # time.sleep(1)
    # Robot.distorqAll()
    # posNow = []
    # dic = {0: 3, 1: 4, 2: 2, 3: 5, 4: 6}
    # for i in range(0, 5):
    #     a = Robot.get(dic[i])
    #     print "Motor"+str(dic[i])+" value = "+str(a)
    #     posNow.append(a)
    #
    # print posNow

    list_id_R = Robot.int_id_R[1:]
    list_id_L = Robot.int_id_L[1:]
    print list_id_L

    kinCal = kinematicsCalculator()
    angle = kinCal.calAngleForLeg(85.0,-85.0,100.0,h=305)
    goal_pos = Robot.moveRobotLegFromAngleInRAD(angle,side='R')
    print "################################\n\n\n\n",goal_pos,'      ',angle,'\n\n\n\n\n\n#########################################'
    Robot.controlSpeedMotor(4,list_id_R,goal_pos)

    print "\n\n\n\n##########################################################stop #############################################################################################\n\n\n\n"
    time.sleep(1)

    goal_pos = [2048,2045,2048,2048,2048]
    Robot.controlSpeedMotor(4,list_id_R,goal_pos)

    angle = kinCal.calAngleForLeg(25.0,-45.0,110.0, h=305)
    goal_pos = Robot.moveRobotLegFromAngleInRAD(angle, side='R')
    print "################################\n\n\n\n", goal_pos, '      ', angle, '\n\n\n\n\n\n#########################################'
    Robot.controlSpeedMotor(4, list_id_R, goal_pos)

    goal_pos = [2048, 2045, 2048, 2048, 2048]
    Robot.controlSpeedMotor(4, list_id_R, goal_pos)

    kinCal = kinematicsCalculator()
    angle = kinCal.calAngleForLeg(85.0, 85.0, 100.0, h=305)
    goal_pos = Robot.moveRobotLegFromAngleInRAD(angle, side='L')
    print "################################\n\n\n\n", goal_pos, '      ', angle, '\n\n\n\n\n\n#########################################'
    Robot.controlSpeedMotor(4, list_id_L, goal_pos)

    print "\n\n\n\n##########################################################stop #############################################################################################\n\n\n\n"
    time.sleep(1)

    goal_pos = [2048, 2048, 2048, 2048, 2048]
    Robot.controlSpeedMotor(4, list_id_L, goal_pos)

    angle = kinCal.calAngleForLeg(25.0, 45.0, 110.0, h=305)
    goal_pos = Robot.moveRobotLegFromAngleInRAD(angle, side='L')
    print "################################\n\n\n\n", goal_pos, '      ', angle, '\n\n\n\n\n\n#########################################'
    Robot.controlSpeedMotor(4, list_id_L, goal_pos)

    goal_pos = [2048, 2048, 2048, 2048, 2048]
    Robot.controlSpeedMotor(4, list_id_L, goal_pos)