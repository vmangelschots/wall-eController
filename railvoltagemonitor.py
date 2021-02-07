import socket

class RailVoltageMonitor():
    def __init__(self):

        self._3vr = 0
        self._5vr = 0
        self._5vr2 = 0


    def updateVoltages(self,threevr,fivevr,fivevr2):

        self._3vr = threevr
        self._5vr = fivevr
        self._5vr2 = fivevr2
    def getVoltages(self):
        return (self._3vr,self._5vr,self._5vr2)