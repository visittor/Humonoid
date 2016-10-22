import serial
import time


class Dynamixel:

    def __init__(self,comPort,baudRate=1000000,timeOut=0.05):
        self.comPort = comPort
        self.baudRate = baudRate
        self.timeOut = timeOut
        self.serial = serial.Serial(self.comPort)
        self.serial.baudrate = self.baudRate

    def WriteData(self,INSTRUCTION_PACKET):
        INSTRUCTION_PACKET.insert(3, len(INSTRUCTION_PACKET)-2)
        CHKSUM = 0
        for i in range(2, len(INSTRUCTION_PACKET)):
            CHKSUM += INSTRUCTION_PACKET[i]
        CHKSUM %= 256
        INSTRUCTION_PACKET.append(255-CHKSUM)
        self.serial.write(INSTRUCTION_PACKET)

    def ReadData(self):
        STATUS_PACKET = []
        start = time.clock()
        while time.clock() - start <= self.timeOut:
            while self.serial.inWaiting():
                STATUS_PACKET.append(ord(self.serial.read()))
        return STATUS_PACKET

    def set_position(self, ID, GOAL=2048, SPEED=0):

        H_GOAL, L_GOAL = divmod(GOAL, 256)
        H_SPEED, L_SPEED = divmod(SPEED, 256)
        if type(ID) is int:
            PACKET = [255, 255, ID, 3, 30, L_GOAL, H_GOAL, L_SPEED, H_SPEED]
            self.WriteData(PACKET)
        else:
            for id in ID:
                PACKET = [255, 255, id, 3, 30, L_GOAL, H_GOAL, L_SPEED, H_SPEED]
                self.WriteData(PACKET)

    def get_position(self, ID):
        if type(ID) is int:
            PACKET = [255, 255, ID, 2, 36, 2]
            self.WriteData(PACKET)
            res = self.ReadData()
            result = res[6]*256+res[5]
            return result
        else:
            result = []
            for id in ID:
                PACKET = PACKET = [255, 255, id, 2, 36, 2]
                self.WriteData(PACKET)
                res = self.ReadData()
                result.append(res[6] * 256 + res[5])
            return result


MX28 = Dynamixel('COM5',1000000)
MX28.set_position([41, 42])
print MX28.get_position([41,42])
time.sleep(1.5)

