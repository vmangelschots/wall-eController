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
        data = self._ipStringToByteArray(server_ip_address)
        sock.sendto(b'C'.join(data), ("192.168.5.186",5006))

    def _ipStringToByteArray(self,ip_address):
        return bytearray(map(int, ip_address.split('.')))
class discoveryServer():
    def __init__(self):
        self.zconf = Zeroconf()
        serviceListener = Listener()
        self.zconf.add_service_listener("_walle._udp.local.",serviceListener)

