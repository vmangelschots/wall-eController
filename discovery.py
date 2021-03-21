from zeroconf import Zeroconf
from threading import Thread
import socket
import logging


class Listener():
    def add_service(self,zeroconf,serviceType,name):
        self.handleNewRobot(zeroconf,serviceType,name)

    def update_service(self,zeroconf,serviceType,name):
        self.handleNewRobot(zeroconf,serviceType,name)

    def handleNewRobot(self,zeroconf,serviceType,name):
        info = zeroconf.get_service_info(serviceType, name)
        ip_address = info.parsed_addresses()[0]
        port = info.port

        hostname = socket.gethostname()
        server_ip_address = socket.gethostbyname(hostname)

        logging.info("New wall-e detected. Address: {}:{}".format(ip_address, port))
        logging.debug("Sending connection info to new wall-e")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = [b'C']
        data.extend(self._ipStringToByteArray(server_ip_address))
        data.append(int(5005).to_bytes(2,byteorder='big'))

        print(data)
        sock.sendto(b''.join(data), (ip_address,5006))

    def _ipStringToByteArray(self,ip_address):
        result = []
        for ip_part in ip_address.split("."):
            result.append(int(ip_part).to_bytes(1,byteorder='big'))
        return result

class discoveryServer():
    def __init__(self):
        self.zconf = Zeroconf()
        serviceListener = Listener()
        self.zconf.add_service_listener("_walle._udp.local.",serviceListener)

