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

from .network  import NetworkConnector
from .messages import MessageFactory
from .exceptions  import *
from . import config

import time
import inspect
import collections

import logging
logger = logging.getLogger(__name__)

class Engine(object):

    def __init__(self,address=config.address,port=config.port,hops=config.hops,key=config.key):

        self.devices = []                        # list of devices / use (un)register_devices()
        self.started = False                     # engine started or not
        self.running = False                     # engine is running or not
        self.timers = []                         # functions to call periodic
        self.__last_timer = 0                    # last timer check
        self.rx_handlers =[self.handle_request]  # message receive workflow


        self.__attributesChange = []             # list of XAALAttributes instances
        self.__txFifo = collections.deque()      # tx msg fifo
        self.__alives = []                       # list of alive devices


        # start network
        self.network = NetworkConnector(address, port, hops)
        # start msg worker
        self.msg_factory = MessageFactory(key)

    #####################################################
    # Devices management
    #####################################################
    def add_device(self, dev):
        """register a new device """
        if dev not in self.devices:
            self.devices.append(dev)
            dev.engine = self

    def add_devices(self, devs):
        """register new devices"""
        for dev in devs:
            self.add_device(dev)

    def remove_device(self, dev):
        """unregister a device """
        dev.engine = None
        # Remove dev from devices list
        self.devices.remove(dev)


    #####################################################
    # xAAL messages Tx handling
    #####################################################
    # Fifo for msg to send
    def queue_msg(self, msg):
        """queue a message"""
        self.__txFifo.append(msg)

    def process_tx_msg(self):
        """ Process (send) message in tx queue called from the loop()"""
        while self.__txFifo:
            temp = self.__txFifo.popleft()
            self.send_msg(temp)

    def send_msg(self, msg):
        """Send an message to the bus, use queue_msg instead"""
        self.network.send(msg)

    def send_request(self,dev,targets,action,body = None):
        """queue a new request"""
        msg = self.msg_factory.build_msg(dev, targets, 'request', action, body)
        self.queue_msg(msg)

    def send_reply(self, dev, targets, action, body=None):
        """queue a new reply"""
        msg = self.msg_factory.build_msg(dev, targets, 'reply', action, body)
        self.queue_msg(msg)

    def send_error(self, dev, errcode, description=None):
        """queue a error message"""
        msg = self.msg_factory.build_error_msg(dev, errcode, description)
        self.queue_msg(msg)

    def send_get_description(self,dev,targets):
        """queue a getDescription request"""
        self.send_request(dev,targets,'getDescription')

    def send_get_attributes(self,dev,targets):
        """queue a getAttributes request"""
        self.send_request(dev,targets,'getAttributes')

    def send_notification(self,dev,action,body=None):
        msg = self.msg_factory.build_msg(dev,[],"notify",action,body)
        self.queue_msg(msg)
        
    #####################################################
    # Alive messages
    #####################################################
    def send_alive(self, dev):
        """Send a Alive message for a given device"""
        timeout = dev.get_timeout()
        msg = self.msg_factory.build_alive_for(dev, timeout)
        self.queue_msg(msg)

    def send_isAlive(self, dev, devtypes):
        """Send a isAlive message, w/ devTypes filtering"""
        body = {}
        body['devTypes'] = devtypes
        msg = self.msg_factory.build_msg(dev, [], "request", "isAlive", body)
        self.queue_msg(msg)

    def process_alives(self):
        """Periodic sending alive messages"""
        now = time.time()
        for dev in self.devices:
            if dev.next_alive < now :
                self.send_alive(dev)
                dev.update_alive()

    #####################################################
    # xAAL attributes changes
    #####################################################
    def add_attributesChange(self, attr):
        """add a new attribute change to the list"""
        self.__attributesChange.append(attr)

    def get_attributesChange(self):
        """return the pending attributes changes list"""
        return self.__attributesChange

    def process_attributesChange(self):
        """Processes (send notify) attributes changes for all devices"""
        devices = {}
        # Group attributes changed by device
        for attr in self.get_attributesChange():
            if attr.device not in devices.keys():
                devices[attr.device] = {}
                devices[attr.device][attr.name] = attr.value
            else:
                # ToDo: test if name keys still exist???
                devices[attr.device][attr.name] = attr.value

        for dev in devices:
            self.send_notification(dev,"attributesChange",devices[dev])
        self.__attributesChange = []  # empty array

    #####################################################
    # xAAL messages rx handlers
    #####################################################
    def receive_msg(self):
        """return new received message or None"""
        result = None
        data = self.network.get_data()
        if data:
            try:
                msg = self.msg_factory.decode_msg(data)
            except MessageParserError as e:
                logger.error(e)
                msg = None
            result = msg
        return result

    def add_rx_handler(self,func):
        self.rx_handlers.append(func)

    def remove_rx_hanlder(self,func):
        self.rx_handlers.remove(func)

    def process_rx_msg(self):
        """process incomming messages"""
        msg = self.receive_msg()
        if msg:
            for func in self.rx_handlers:
                func(msg)

    def handle_request(self, msg):
        """Filter msg for devices according default xAAL API then process the
        request for each targets identied in the engine
        """
        if msg.is_request():
            targets = filter_msg_for_devices(msg, self.devices)
            if targets:
                self.process_request(msg, targets)

    def process_request(self, msg, targets):
        """Processes request by device and add related response
        if reply necessary in the Tx fifo

        Note: xAAL attributes change are managed separately
        """
        for target in targets:
            if msg.action == 'isAlive':
                self.send_alive(target)
            else:
                self.handle_method_request(msg, target)

    def handle_method_request(self, msg, target):
        """Run method (xAAL exposed method) on device:
            - None is returned if device method do not return anything
            - result is returned if device method gives a response
            - Errors are raised if an error occured:
                * Internal error
                * error returned on the xAAL bus
        """
        try:
            result = run_action(msg, target)
            if result != None:
                self.send_reply(dev=target,targets=[msg.source],action=msg.action,body=result)
        except DeviceError as e:
            self.send_error(target, e.code, e.description)
        except XAALError as e:
            logger.error(e)

    #####################################################
    # timers
    #####################################################
    def add_timer(self,func,period,repeat=-1):
        t = Timer(func,period,repeat)
        self.timers.append(t)

    def remove_timer(self,timer):
        self.timers.remove(timer)

    def process_timers(self):
        expire_list = []
        
        if len(self.timers)!=0 :
            now = time.time()
            # little hack to avoid to check timer to often.
            # w/ this enable timer precision is bad, but far enougth
            if (now - self.__last_timer) < 0.4: return

            for t in self.timers:
                if t.deadline < now:
                    try:
                        t.func()
                    except CallbackError as e:
                        logger.error(e.description)
                    if (t.repeat != -1):
                        t.repeat = t.repeat-1
                        if t.repeat == 0:
                            expire_list.append(t)
                    t.deadline = now + t.period
            # delete expired timers
            for t in expire_list:
                self.remove_timer(t)
                    
            self.__last_timer = now

    #####################################################
    # Mainloops & run ..
    #####################################################
    def loop(self):
        """Process incomming xAAL msg
        Process attributes change for device
        Process timers
        Process isAlive for device
        Send msgs from the Tx Buffer
        """

        # Process xAAL msg received, filter msg and process request
        self.process_rx_msg()

        # Process attributes change for devices
        self.process_attributesChange()

        # Process timers
        self.process_timers()

        # Process Alives
        self.process_alives()

        # Process xAAL msgs to send
        self.process_tx_msg()

    def start(self):
        """Start the core engine: send queue alive msg"""
        if self.started:
            return
        self.network.connect()
        for dev in self.devices:
            self.send_alive(dev)
            dev.update_alive()
        self.started = True

    def stop(self):
        self.running = False

    def run(self):
        self.start()
        self.running = True
        while self.running:
            self.loop()


def filter_msg_for_devices(msg, devices):
    """loop throught the devices, to find which are
    expected w/ the msg

    - Filter on devTypes for isAlive request.
    - Filter on device address
    """
    results = []
    if msg.action == 'isAlive':
        if 'devTypes' in msg.body.keys():
            devtypes = msg.body['devTypes']
            if 'any.any' in devtypes:
                results = devices
            else:
                for dev in devices:
                    any_subtype = dev.devtype.split('.')[0] + '.any'
                    if dev.devtype in devtypes:
                        results.append(dev)
                    elif any_subtype in devtypes:
                        results.append(dev)
    else:
        if not msg.targets:  # if target list is empty == broadcast
            results = devices
        else:
            for dev in devices:
                if dev.address in msg.targets:
                    results.append(dev)
    return results


def run_action(msg, device):
    """Extract & run an action (match with exposed method) from a msg
    on the selected device.
    Return:
        - None
        - result from method if method return something

    Note: If action not found raise error, if wrong parameter raise error
    """
    methods = device.get_methods()
    params = {}
    result = None
    if msg.action in methods.keys():
        method = methods[msg.action]
        body_params = None
        if msg.body:
            method_params = get_args_method(method)
            body_params = msg.get_parameters()

            for k in body_params:
                temp = '_%s' %k
                if temp in method_params:
                    params.update({temp:body_params[k]})
                else:
                    logger.info("Wrong method parameter [%s] for action %s" %(k, msg.action))
        try:
            result = method(**params)
        except :
            raise XAALError("Error in method:%s params:%s" % (msg.action,params))
    else:
        raise XAALError("Method %s not found" % msg.action)
    return result

def get_args_method(method):
    """ return the list on arguments for a given method """
    spec = inspect.getargspec(method)
    try:
        spec.args.remove('self')
    except:
        pass
    return spec.args


class Timer(object):
    def __init__(self,func,period,repeat):
        self.func = func
        self.period = period
        self.repeat = repeat
        self.deadline = 0
        
