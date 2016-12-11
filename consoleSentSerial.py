import serial
import time
#test git
class SentData(object):

    def __init__(self,com,baurd = 9600):
        self.ser = serial.Serial(com)
        self.ser.baudrate = baurd
        self.timeout = 0.05

    def sent(self,package):
        self.ser.write(package)
        print'\n\n////////////////\ndone\n////////////////\n\n'

    def readData(self):
        packet = []
        startTime = time.clock()
        while time.clock() - startTime <= self.timeout:
            while self.ser.inWaiting():
                packet.append(ord(self.ser.read()))
        return packet

if __name__ == '__main__':

    com = raw_input('Select COM port')
    listSetting = com.split(' ')
    if len(listSetting) == 2:
        sender = SentData(listSetting[0],baurd=listSetting[1])
    elif len(listSetting) == 1:
        sender = SentData(listSetting[0])

    else:
        print 'Unexpected parameter'
    def sentDATA():
        a = raw_input('Input command')
        listCommand = a.split('-')
        if len(listCommand) > 2:
            print 'Syntax error'

        else:
            if listCommand[0].lower() == 'sent':
                p = listCommand[1].split(' ')
                error = False
                package = []
                for i in p:
                    try:
                        package.append(int(i))
                    except ValueError:
                        print 'cant be send'
                        error = True
                        break

                if error:
                    pass

                else:
                    sender.sent(package)

            elif listCommand[0].lower() == 'recieve':
                print 'ok'
            else:
                print 'no command'

    while True:
        package = ''
        package = sender.readData()
        if len(package) != 0:
            print ( package)

        try:
            print 'not interupt'
            package = ''
            package = sender.readData()
            if len(package)>0:
                print '\n\n', package, '\n\n'
        except (KeyboardInterrupt,sentDATA):
            print 'interupt'
            a = raw_input('Input command')
            listCommand = a.split('-')
            if len(listCommand) > 2:
                print 'Syntax error'

            else:
                if listCommand[0].lower() == 'sent':
                    p = listCommand[1].split(' ')
                    error = False
                    package = []
                    for i in p:
                        try:
                            package.append(int(i))
                        except ValueError:
                            print 'cant be send'
                            error = True
                            break

                    if error:
                        pass

                    else:
                        sender.sent(package)

                elif listCommand[0].lower() == 'recieve':
                    print 'ok'
                else:
                    print 'no command'

