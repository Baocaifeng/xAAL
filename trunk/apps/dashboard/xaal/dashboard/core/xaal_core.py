from xaal.lib import tools,Engine,Device
from xaal.monitor import Monitor
from . import sio

import platform
from gevent import Greenlet

import time

# dev-type that don't appear in results
BLACK_LIST=['cli.experimental',]

PACKAGE_NAME = "xaal.dashboard"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

# we use this global variable to share data with greenlet
monitor = None

# used for uptime
started = time.time()

def monitor_filter(msg):
    """ Filter incomming messages. Return False if you don't want to use this device"""
    if msg.devtype in BLACK_LIST:
        return False
    return True

def event_handler(ev_type,dev):
    print("Event %s %s" % (ev_type,dev))
    msg = { 'address': dev.address,'attributes':dev.attributes}
    sio.broadcast('event_attributeChanges',msg)

    
def setup():
    """ setup xAAL Engine & Device. And start it in a Greenlet"""
    global monitor 
    engine = Engine()
    cfg = tools.load_cfg_or_die(PACKAGE_NAME)

    dev            = Device("hmi.basic")
    dev.address    = cfg['config']['addr']
    dev.vendor_id  = "IHSEV"
    dev.product_id = "WEB Interface"
    dev.version    = 0.1
    dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())

    engine.add_device(dev)
    monitor = Monitor(dev,filter_func=monitor_filter)
    monitor.subscribe(event_handler)
    
    engine.start()        
    green_let = Greenlet(xaal_loop, engine)
    green_let.start()

def xaal_loop(engine):
    """ xAAL Engine Loop Greenlet"""
    while 1:
        engine.loop()

def send_request(addr,action,body):
    eng = monitor.dev.engine
    eng.send_request(monitor.dev,[addr],action,body)
        

def get_uptime():
    return int(time.time() - started)


def get_device(addr):
    return monitor.devices.get_with_addr(addr)
