import cv2
import numpy as np
import json
import pickle
import socket
import struct

class getData:
    def __init__(self,port = 1506,host_ = None):
        self.s = socket.socket()
        if host_ is None:
            host = socket.gethostbyname(socket.gethostname())
        else:
            host = host_
        self.s.connect((host,port))
        self.data2return=(None,None,None,None,None,None)

    def reciev(self):
        data = ""
        payLoad_size = struct.calcsize('L')
        # print payLoad_size
        massage = 1
        try:
            self.s.send('request')
            mssg = self.s.recv(4096)
            if mssg  == 'begin':
                mssg = self.s.recv(4096)
                # print '***',mssg[4]
                # while len(data)<payLoad_size:
                #     print len(mssg)
                #     data += mssg[i]
                #     if len(data)>=payLoad_size:
                #         break
                #     i += 1
                #     # print data
                # packed_mssg_size = mssg[:payLoad_size]
                # data = mssg[payLoad_size:]
                # mssg_size = struct.unpack('L',packed_mssg_size)[0]
                # while len(data)<mssg_size:
                #     data += mssg[i]
                #     i += 1
                # massage = data[:mssg_size]
                # data = ''
                # print '*************************************************'
                # while len(data)<payLoad_size:
                #     data += self.s.recv(4096)
                #     print data
                # packed_mssg_size = data[:payLoad_size]
                # data = data[payLoad_size:]
                # mssg_size = struct.unpack('L',packed_mssg_size)[0]
                # while len(data)<mssg_size:
                #     data += self.s.recv(4096)
                # mssg = data[:mssg_size]
                # data = data[:mssg_size]
        except socket.error:
            return False


        if not mssg:
            return False
        elif mssg == 'recieve':
            return False
        elif massage is not None:
            self.data2return = pickle.loads(mssg)
            try:
                self.data2return = pickle.loads(mssg)
                return True
            except ValueError:
                print 'Error'
                return False
        else:
            return False

    def getData(self):
        return self.data2return[0]

    def getOuter(self):
        return self.data2return[1]

    def getInner(self):
        return self.data2return[2]

    def getCenter(self):
        return self.data2return[3]

    def getRadius(self):
        return self.data2return[4]

    def getFrame(self):
        if self.data2return[-1] is not None:
            # nparr = np.fromstring(self.data2return[-1], np.uint8)
            # return cv2.imdecode(nparr,1)
            return self.data2return[-1]


if __name__ == "__main__":
    reciever = getData()
    while True:
        if reciever.reciev():
            # pass
            print reciever.getData()
        cv2.waitKey(1)
