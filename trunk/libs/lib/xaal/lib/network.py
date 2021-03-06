# -*- coding: utf-8 -*-

#
#  Copyright 2014, Jérôme Colin, Jérôme Kerdreux, Philippe Tanguy,
#  Telecom Bretagne.
#
#  This file is part of xAAL.
#
#  xAAL is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  xAAL is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with xAAL. If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function

import socket
import struct
import select
import codecs

import logging

logger = logging.getLogger(__name__)

import time
from enum import Enum

class NetworkState(Enum):
    disconnected = 0
    connected    = 1


class NetworkConnector(object):
    UDP_MAX_SIZE = 65507

    def __init__(self, addr, port, hops):
        self.addr = addr
        self.port = port
        self.hops = hops
        self.state = NetworkState.disconnected

    def connect(self):
        try:
            self.__connect()
        except Exception as e:
            self.network_error(e)

    def __connect(self):
        logger.info("Connecting to %s:%s" % (self.addr, self.port))
        # TBD add bind_addr attrib
        bind_addr = ''

        self.__sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        # self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # #formac os ???
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((bind_addr, self.port))
        mreq = struct.pack('4sl',socket.inet_aton(self.addr),socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)
        self.__sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,self.hops)
        self.state = NetworkState.connected

    def disconnect(self):
        logger.info("Disconnecting from the bus")
        self.state = NetworkState.disconnected
        self.__sock.close()

    def is_connected(self):
        return self.state == NetworkState.connected

    def receive(self):
        packt = self.__sock.recv(self.UDP_MAX_SIZE)
        return packt

    def __get_data(self):
        r = select.select([self.__sock, ], [], [], 0.03)
        if r[0]:
            return self.receive()
        return None

    def get_data(self):
        if not self.is_connected(): self.connect()
        try:
            return self.__get_data()
        except Exception as e:
            self.network_error(e)

    def send(self, message):
        if not self.is_connected(): self.connect()
        try:
            self.__sock.sendto(codecs.encode(message), (self.addr, self.port))
        except Exception as e:
            self.network_error(e)

    def network_error(self, msg):
        self.disconnect()
        logger.info("Network error, reconnect..%s" % msg)
        time.sleep(5)
