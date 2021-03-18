from zeroconf import Zeroconf
from threading import Thread

class Listener():
    def add_service(self,zeroconf,serviceType,name):
        info = zeroconf.get_service_info(serviceType, name)

        print("Address: " + str(info.parsed_addresses()))
        print("Port: " + str(info.port))
        print("Service Name: " + info.name)
        print("Server: " + info.server)
        print("Properties: " + str(info.properties))

class discoveryServer():
    def __init__(self):
        self.zconf = Zeroconf()
        serviceListener = Listener()
        self.zconf.add_service_listener("_walle._udp.local.",serviceListener)

