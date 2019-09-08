from threading import Thread
import threading
from PyQt5.QtCore import *
import logging
import socket
import ifcfg
import time

import google.protobuf
from PyQt5 import QtCore
import Vision.proto.messages_robocup_ssl_wrapper_pb2 as wrapper
import Vision.proto.messages_robocup_ssl_detection_pb2 as detect



log = logging.getLogger('vision')
FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)


class Vision(QtCore.QThread):
    graphic_ready = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        print("Vision")

        self._IP = "224.5.23.2"
        self._PORT = 10020
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)

        self.__inet = ifcfg.interfaces()['wlp3s0']['inet']

        self.__sock.setsockopt(socket.IPPROTO_IP,
                               socket.IP_ADD_MEMBERSHIP,
                               socket.inet_aton(self._IP) + socket.inet_aton(self.__inet))

        self.__BUFFER_SIZE = 2048
        self.__wrapper = wrapper.SSL_WrapperPacket()
        self.__detect = detect.SSL_DetectionFrame()
        self.last = time.time()

        self.__isConnected = False

        # self.connect()

    def connect(self):
        if self.__sock:
            self.__sock.bind((self._IP, self._PORT))
            print("Connection Established.")
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
            raw_data = self.__sock.recvfrom(self.__BUFFER_SIZE)
        except KeyboardInterrupt:
            self.disconnect()
            exit(0)

        try:
            self.__wrapper.ParseFromString(raw_data[0])
            self.graphic_ready.emit([self.__wrapper.geometry, self.__wrapper.detection])

        except google.protobuf.message.DecodeError:
            print("Error")

    def run(self):
        while True:
            self.recv()

    def isConnected(self):
        return self.__isConnected