# -*- coding: utf-8 -*-

#
#  Copyright 2014, Jérôme Colin, Jérôme Kerdreux, Philippe Tanguy,
# Telecom Bretagne.
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


from . import tools
from . import config
from .exceptions import MessageError,MessageParserError

import ujson as json
import datetime
import pysodium
import base64
import struct
import sys

import logging
logger = logging.getLogger(__name__)


class MessageFactory(object):
    """Message Factory:
    - Build xAAL message
    - Apply security layer, Ciphering/De-Ciphering chacha20 poly1305
    - Serialize/Deserialize data in JSON"""

    def __init__(self, cipher_key):
        self.cipher_key = cipher_key    # key encode / decode message built from passphrase


    def encode_msg(self, msg):
        """Apply security layer and return encode MSG in Json
        :param msg: xAAL msg instance
        :type msg: Message
        :return: return an xAAL msg ciphered and serialized in json
        :rtype: json
        """
        result = {}

        # Format data msg to send
        result['version'] = msg.version
        result['targets'] = json.dumps(msg.targets)
        result['timestamp'] = msg.timestamp

        # Format payload before ciphering
        if msg.body:
            buf = json.dumps({"header": msg.header, "body": msg.body})
        else:
            buf = json.dumps({"header": msg.header})

        # Payload Ciphering: ciph
        # Additionnal Data == json serialization of the targets array
        payload = buf.encode('utf-8')
        ad      = json.dumps(msg.targets).encode('utf-8')  # Additional Data
        nonce   = build_nonce(msg.timestamp)
        ciph    = pysodium.crypto_aead_chacha20poly1305_ietf_encrypt(payload, ad, nonce, self.cipher_key)

        # Add payload: base64 encoded of payload cipher
        result['payload'] = base64.b64encode(ciph)

        # Json serialization
        return json.dumps(result)

    def decode_msg(self, data):
        """Decode incoming Json data and De-Ciphering
        :param data: data received from the multicast bus
        :type data: json
        :return: xAAL msg
        :rtype: Message
        """
        # Decode json incoming data
        try:
            data_rx = json.loads(data)
        except:
            raise MessageParserError("Unable to parse JSON data")

        # Instanciate Message
        msg = Message()
        try:
            msg.targets = json.loads(data_rx['targets'])
            msg.version = data_rx['version']
            msg_time    = data_rx['timestamp'][0]
        except (KeyError, IndexError):
            raise MessageParserError("Bad Message, wrong fields")

        # Replay attack, window fixed to CIPHER_WINDOW in seconds
        now = build_timestamp()[0]  # test done only on seconds ...

        if msg_time < (now - config.cipher_window):
            raise MessageParserError("Potential replay attack, message too old")

        if msg_time > (now + config.cipher_window):
            raise MessageParserError("Potential replay attack, message too young")

        # Payload De-Ciphering
        ad = data_rx['targets'].encode("utf8")  # Additional Data
        nonce = build_nonce(data_rx['timestamp'])

        # base64 decoding
        if 'payload' in data_rx:
            ciph = base64.b64decode(data_rx['payload'])
        else:
            raise MessageParserError("Bad Message, no payload found!")

        # chacha20 deciphering
        try:
            pjson = pysodium.crypto_aead_chacha20poly1305_ietf_decrypt(ciph, ad, nonce, self.cipher_key)
        except :
            raise MessageParserError("Unable to decrypt msg")

        # Decode Json
        try:
            payload = json.loads(pjson)
        except:
            raise MessageParserError("Unable to parse JSON data in payload after decrypt")

        # Message unpacking header
        if 'header' in payload:
            head = {}
            for (name, value) in payload["header"].items():
                head[name] = value
            msg.header = head
        else:
            raise MessageParserError("Bad Message, none header found in payload!")

        # Message unpacking body
        if 'body' in payload:
            body = {}
            for (name, value) in payload["body"].items():
                body[name] = value
            msg.body = body

        return msg

    #####################################################
    # MSG builder
    #####################################################
    def build_msg(self,dev=None,targets=[], msgtype=None,action=None,body=None):
        """ the build method takes in parameters :\n
             -A device\n
             -The list of targets of the message\n
             -The type of the message\n
             -The action of the message\n
             -A body if it's necessary (None if not)
             it will return a message encoded in Json and Ciphered.
        """
        message = Message()
        if dev:
            message.source = dev.address
            message.devtype = dev.devtype

        message.targets = targets
        message.timestamp = build_timestamp()

        if msgtype:
            message.msgtype = msgtype
        if action:
            message.action = action
        if body is not None and body != {}:
            message.body = body

        data = self.encode_msg(message)
        return data

    def build_alive_for(self, dev, timeout=0):
        """ Build Alive message for a given device
        timeout = 0 is the minimum value
        """
        body = {}
        body['timeout'] = timeout
        message = self.build_msg(dev=dev,targets=[],msgtype="notify",action="alive",body=body)
        return message

    def build_error_msg(self, dev, errcode, description=None):
        """ Build a Error message """
        message = Message()
        body = {}
        body['code'] = errcode
        if description:
            body['description'] = description
        message = self.build_msg(dev, [], "notify", "error", body)
        return message




class Message(object):
    """ Message object used for incomming & outgoint message """

    def __init__(self):
        self.body = {}                       # message body
        self.header = {}                     # dict used to store msg headers
        self.timestamp = None                # message timestamp
        self.version = config.STACK_VERSION  # message API version
        self.__targets = []                  # target property

    def __get_header_value(self, key):
        """ hack to avoid missing keys in header """
        # drop KeyError while playing w/ message keys
        if key in self.header.keys():
            return self.header[key]
        return None

    @property
    def targets(self):
        return self.__targets

    @targets.setter
    def targets(self, values):
        if not isinstance(values, list):
            raise TypeError("Expected a list for targetsList, got %s" % (type(values),))
        for val in values:
            if not tools.is_valid_addr(val):
                raise MessageError("Bad target addr: %s" % val)
        self.__targets = values

    @property
    def devtype(self):
        return self.__get_header_value('devType')

    @devtype.setter
    def devtype(self, value):
        self.header['devType'] = value

    @property
    def source(self):
        return self.__get_header_value('source')

    @source.setter
    def source(self, value):
        self.header['source'] = value

    @property
    def msgtype(self):
        return self.__get_header_value('msgType')

    @msgtype.setter
    def msgtype(self, value):
        self.header['msgType'] = value

    @property
    def action(self):
        return self.__get_header_value('action')

    @action.setter
    def action(self, value):
        self.header['action'] = value


    #####################################################
    # Body
    #####################################################
    def _get_parameters(self, args):
        parameters = {}
        for p in range(0, len(args)):
            if isinstance(self.body[args[p]], str):
                param = "'%s'" % self.body[args[p]]
            else:
                param = self.body[args[p]]

            parameters[args[p]] = param
        return parameters

    def get_parameters(self):
        """ request parameters are in body hash, return asis"""
        return self.body

    #####################################################
    def dump(self):
        """ dump log a message """
        logger.debug("== Message (0x%x) ======================" % id(self))
        logger.debug("*****Header*****")
        if 'devType' in self.header:
            logger.debug("devType \t%s" % self.devtype)
        if 'action' in self.header:
            logger.debug("action: \t%s" % self.action)
        if 'msgType' in self.header:
            logger.debug("msgType: \t%s" % self.msgtype)
        if 'source' in self.header:
            logger.debug("source: \t%s" % self.source)
        logger.debug("version: \t%s" % self.version)
        logger.debug("targets: \t%s" % self.targets)

        if self.body:
            logger.debug("*****Body*****")
            logger.debug("%s \t" % self.body)

    def __str__(self):
        l = ["<Message (0x%x)>" % id(self),]
        if 'source'  in self.header: l.append(self.source)
        if 'devType' in self.header: l.append(self.devtype)
        if 'msgType' in self.header: l.append(self.msgtype)
        if 'action'  in self.header: l.append(self.action)
        if self.body: l.append(str(self.body))
        return " ".join(l)

    def is_request(self):
        if self.msgtype == 'request':
            return True
        return False

    def is_reply(self):
        if self.msgtype == 'reply':
            return True
        return False

    def is_notify(self):
        if self.msgtype == 'notify':
            return True
        return False

    def is_alive(self):
        if self.msgtype == 'notify' and self.action == 'alive':
            return True
        return False

    def is_attributes_change(self):
        if self.msgtype == 'notify' and self.action == 'attributesChange':
            return True
        return False

    def is_get_attribute_reply(self):
        if self.msgtype == 'reply' and self.action == 'getAttributes':
            return True
        return False

    def is_get_description_reply(self):
        if self.msgtype == 'reply' and self.action == 'getDescription':
            return True
        return False



def build_nonce(data):
    """ Big-Endian, time in seconds and time in microseconds """
    nonce = struct.pack('>QL', data[0], data[1])
    return nonce


def build_timestamp():
    """Return array [seconds since epoch, microseconds since last seconds] Time = UTC+0000"""
    epoch = datetime.datetime.utcfromtimestamp(0)
    timestamp = datetime.datetime.utcnow() - epoch
    return _packtimestamp(timestamp.total_seconds(), timestamp.microseconds)


# for better performance, I choose to use this trick to fix the change in size for Py3.
# only test once.
if sys.version_info.major == 2:
    _packtimestamp = lambda t1,t2: [long(t1),int(t2)]
else:
    _packtimestamp = lambda t1,t2: [int(t1),int(t2)]
