import socket
from threading import Thread


UDP_IP = "0.0.0.0"
UDP_PORT = 5005


class CommandServer():
    def __init__(self):
        self._serverThread = Thread(target=self.serverThread)
        self._serverThread.start()
        self.servoChannels = [
           128,128,128,128,128,128,128
        ]

    def setServoChannel(self,index,value):
        self.servoChannels[index-1] = value
    def serverThread(self):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_PORT))

        sock2 = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            print(data)
            if(data[0]==99):
                adc0 = int.from_bytes(data[1:3],byteorder='big')
                adc1 = int.from_bytes(data[3:5],byteorder='big')
                adc2 = int.from_bytes(data[5:7],byteorder='big')
                print("voltage: {} {} {}".format(adc0*3,adc1*3,adc2*3))
            else:
                print('unkown command')
            data = [b"S"]
            for channel in self.servoChannels:
                data.append(channel.to_bytes(1,'big'))
            sock2.sendto(b''.join(data),("192.168.5.177",5006))