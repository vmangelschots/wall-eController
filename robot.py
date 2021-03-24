import socket
from threading import Thread
from time import sleep


UDP_IP = "0.0.0.0"
UDP_PORT = 5005


class Robot(object):
    LEFT_ARM = "left_arm"
    RIGHT_ARM = "right_arm"
    NECK_HEIGHT = "neck_height"
    NECK_TILT = "neck_tilt"
    HEAD_ROTATION = "head_rotation"
    EYE_ROTATION = "eye_rotation"
    LEFT_EYE = "left_eye"
    RIGHT_EYE = "right_eye"
    LEFT_TRACK = "left_track"
    RIGHT_TRACK = "right_track"

    def __init__(self):
        self.is_configured = False
        self.is_connected = False
        self.servo_channels = [
            128,
            128,
            128,
            128,
            128,
            128,
            128,
            128
        ]
        self.motor_channels = [
            128,
            128
        ]
        self.partToChannelmapping = {
            self.LEFT_ARM: 0,
            self.RIGHT_ARM: 1,
            self.NECK_HEIGHT: 2,
            self.NECK_TILT: 3,
            self.HEAD_ROTATION: 4,
            self.EYE_ROTATION: 5,
            self.LEFT_EYE: 6,
            self.RIGHT_EYE: 7
        }

        self.trackToChannelMapping = {
            self.LEFT_TRACK: 0,
            self.RIGHT_TRACK: 1
        }
        self.startRobotServer()

    def _raw_relative_move_servo(self,channel,ammount):
         current_position = self.servo_channels[channel]
         current_position += ammount
         current_position = max(ammount,0)
         current_position = min(ammount,255)
         self._raw_absolute_move_servo(channel, current_position)

    def _raw_absolute_move_servo(self, channel, current_position):
        self.servo_channels[channel] = current_position

    def _raw_relative_move_motor(self,channel,ammount):
        current_position = self.motor_channels[channel]
        current_position += ammount
        current_position = max(ammount, 0)
        current_position = min(ammount, 255)
        self.raw_absolute_move_motor(channel, current_position)

    def _raw_absolute_move_motor(self, channel, current_position):
        self.motor_channels[channel] = current_position

    def relative_move_part(self,part,ammount):
        self._raw_relative_move_servo(self.partToChannelmapping[part], ammount)

    def relative_move_track(self,track,ammount):
        self._raw_relative_move_motor(self.trackToChannelMapping[track],ammount)

    def absolute_move_part(self,part,position):
        position = max(0,position)
        position = min(255,position)
        self._raw_absolute_move_servo(self.partToChannelmapping[part],position)

    def absolute_move_track(self,track,position):
        position = max(0,position)
        position = min(255,position)
        self._raw_absolute_move_motor(self.trackToChannelMapping[track],position)

    def startRobotServer(self):
        self._serverThread = Thread(target=self.serverReceiveThread)
        self._serverThread.start()
        self._serverSendThread = Thread(target=self.serverSendThread)
        self._serverSendThread.start()

    def serverReceiveThread(self):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_PORT))


        while True:
            if(not self.is_connected):
                sleep(0.25)
                continue
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            #print(data)
            if(data[0]==99):
                adc0 = int.from_bytes(data[1:3],byteorder='big')
                adc1 = int.from_bytes(data[3:5],byteorder='big')
                adc2 = int.from_bytes(data[5:7],byteorder='big')
                cell1 = int.from_bytes(data[7:9],byteorder='big')
                cell2 = int.from_bytes(data[9:11],byteorder='big')
                cell3 = int.from_bytes(data[11:13],byteorder='big')
                print("voltage: {} {} {} {} {} {}".format(adc0*3,adc1*3,adc2*3,cell1*3,cell2*3,cell3*3))
            else:
                print('unkown command')
    def serverSendThread(self):


        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        while True:
            if(not self.is_connected):
                sleep(0.25)
                continue
            data = [b"S"]
            for channel in self.servo_channels[:-1]:
                data.append(channel.to_bytes(1,'big'))
            for channel in self.motor_channels:
                data.append(channel.to_bytes(1,'big'))
            sock.sendto(b''.join(data),(self.ip_address,self.port))
            #print("sending {}".format(data))
    def setConnectionInfo(self,ip_address,port):
        self.is_connected = True
        self.ip_address = ip_address
        self.port = port

TheBot = Robot()