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


from . import config
from . import tools
from .exceptions import DeviceError

import logging
logger = logging.getLogger(__name__)

import time

class Attribute(object):

    def __init__(self, name, dev=None, default=None):
        self.name = name
        self.default = default
        self.device = dev
        self.__value = default

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value != self.__value:
            eng = self.device.engine
            if eng:
                eng.add_attributesChange(self)
                logger.debug("Attr change %s=%s" % (self.name,value))
        self.__value = value

    def __str__(self):
        return "attr: %s  value: %s" % (self.name, self.value)


class Attributes(list):
    
    def __getitem__(self,value):
        if isinstance(value,int):
            return list.__getitem__(self,value)
        for k in self:
            if (value == k.name):
                return k.value
        raise KeyError(value)
    
    def __setitem__(self,name,value):
        if isinstance(name,int):
            return list.__setitem__(self,name,value)
        for k in self:
            if (name == k.name):
                k.value = value
                return
        raise KeyError(name)
                
    
class Device(object):

    def __init__(self,devtype,addr=None,engine=None):
        self.devtype = devtype          # xaal devtype
        self.address = addr             # xaal addr

        self.vendor_id = None           # vendor ID ie : ACME
        self.product_id = None          # product ID
        self.version = None             # product release
        self.url = None                 # product URL
        self.info = None                # additionnal info
        self.hw_id = None               # hardware info
        self.group_id = None            # group devices

        self.unsupported_attributes = []
        self.unsupported_methods = []
        self.unsupported_notifications = []

        self.alive_period = config.alive_timer # time in sec between two alive
        self.next_alive = 0

        self.__attributes = Attributes()

        self.new_attribute('busAddr',config.address)
        self.new_attribute('busPort',config.port)
        self.new_attribute('hops',config.hops)

        self.methods = {'getAttributes' : self._get_attributes,
                        'getDescription': self._get_description }
        self.engine = engine

    @property
    def devtype(self):
        return self.__devtype

    @devtype.setter
    def devtype(self, value):
        if not tools.is_valid_devtype(value):
            raise DeviceError("The devtype %s is not valid" % value)
        self.__devtype = value

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        # version must be a string
        if value:
            self.__version = "%s" % value
        else:
            self.__version = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        if value == None:
            self.__address = None
            return
        if not tools.is_valid_addr(value):
            raise DeviceError("This address is not valid")
        if value == config.XAAL_BCAST_ADDR:
            raise DeviceError("This address is reserved")
        self.__address = value


    # attributes
    def new_attribute(self,name,default=None):
        attr = Attribute(name,self,default)
        self.add_attribute(attr)
        return attr

    def add_attribute(self, attr):
        if attr:
            self.__attributes.append(attr)
            attr.device = self

    def get_attribute(self,name):
        for attr in self.__attributes:
            if attr.name == name:
                return attr
        return None

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self,values):
        if isinstance(values,Attributes):
            self.__attributes = values
        else:
            raise DeviceError("Invalid attributes list, use class Attributes)")

    def add_method(self,name,func):
        self.methods.update({name:func})

    def get_methods(self):
        return self.methods

    def update_alive(self):
        """ update the alive timimg"""
        self.next_alive = time.time() + self.alive_period

    def get_timeout(self):
        """ return Alive timeout used for isAlive msg"""
        return 2 * self.alive_period

    #####################################################
    # Usefull methods
    #####################################################
    def dump(self):
        print("========= %s =========" % self)
        print("Type:\t\t%s" % self.devtype)
        if self.address:
            print("Address: \t%s" % self.address)
        print("Version: \t%s" % self.version)
        print("Info: \t%s" % self.info)


    #####################################################
    # default public methods
    #####################################################
    def _get_description(self):
        result = {}
        if self.vendor_id:  result['vendorId']  = self.vendor_id
        if self.product_id: result['productId'] = self.product_id
        if self.version:    result['version']   = self.version
        if self.url:        result['url']       = self.url
        if self.info:       result['info']      = self.info
        if self.hw_id:      result['hwId']     = self.hw_id
        if self.group_id:   result['groupId']   = self.group_id
        result['unsupportedMethods']            = self.unsupported_methods
        result['unsupportedNotifications']      = self.unsupported_notifications
        result['unsupportedAttributes']         = self.unsupported_attributes
        return result

    def _get_attributes(self, _attributes=None):
        """
        attributes:
            - None = body empty and means request all attributes
            - Empty array means request all attributes
            - Array of attributes (string) and means request attributes in the
              list

        TODO: (Waiting for spec. decision) add test on attribute devices
            - case physical sensor not responding or value not ready add error
            with specific error code and with value = suspicious/stale/cached
        """
        result = {}
        dev_attr = {attr.name: attr for attr in self.__attributes}
        if _attributes:
            """Process attributes filter"""
            for attr in _attributes:
                if attr in dev_attr.keys():
                    result.update({dev_attr[attr].name: dev_attr[attr].value})
                else:
                    logger.debug("Attribute %s not found" % attr)
        else:
            """Process all attributes"""
            for attr in dev_attr.values():
                result.update({attr.name: attr.value})
        return result
