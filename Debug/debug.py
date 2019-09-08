import logging
import socket
import ifcfg
import time
import google.protobuf
from PyQt5 import QtCore
from Debug.proto.data_plot_pb2 import *

log = logging.getLogger('Debugger')
FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)


class debug(QtCore.QThread):
    graphic_ready = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        log.info("Start")

        self._IP = "224.5.23.5"
        self._PORT = 30008
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

        self.__inet = ifcfg.interfaces()['wlp3s0']['inet']

        self.__sock.setsockopt(socket.IPPROTO_IP,
                               socket.IP_ADD_MEMBERSHIP,
                               socket.inet_aton(self._IP) + socket.inet_aton(self.__inet))

        self.__BUFFER_SIZE = 2048

        self.__isConnected = False


    def connect(self):
        if self.__sock:
            self.__sock.bind((self._IP, self._PORT))
            log.info("Connection Established.")
            self.__isConnected = True

    def disconnect(self):
        try:
            self.__sock.close()
            self.__isConnected = False
        except socket.error:
            print(":)")

    def recv(self):
        raw_data = 0
        try:
            raw_data = self.__sock.recvfrom(self.__BUFFER_SIZE)[0]
        except KeyboardInterrupt:
            self.disconnect()
            exit(0)

        try:
            data = data_gram()
            data.ParseFromString(raw_data)
            data_pack = data.data_package
            name = None
            if data_pack.HasField('name'):
                name = data_pack.name
            data = data_pack.y

            self.graphic_ready.emit([name, data])

        except google.protobuf.message.DecodeError:
            print("Error")

    def run(self):
        while True:
            self.recv()

    def isConnected(self):
        return self.__isConnected

