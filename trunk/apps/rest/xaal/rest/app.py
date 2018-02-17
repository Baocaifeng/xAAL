from gevent import monkey; monkey.patch_all()


from xaal.lib import tools,Engine,Device
from xaal.monitor import Monitor

from bottle import default_app,debug,get,response,redirect,static_file

import json
import os
import platform

from gevent import Greenlet
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler


# dev-type that don't appear in results
BLACK_LIST=['cli.experimental',]

PACKAGE_NAME = "xaal.rest"
logger = tools.get_logger(PACKAGE_NAME,'INFO')

# we use this global variable to share data with greenlet
monitor = None


def monitor_filter(msg):
    """ Filter incomming messages. Return False if you don't want to use this device"""
    if msg.devtype in BLACK_LIST:
        return False
    return True


def setup_xaal():
    """ setup xAAL Engine & Device. And start it in a Greenlet"""
    global monitor 
    engine = Engine()
    cfg = tools.load_cfg_or_die(PACKAGE_NAME)

    dev            = Device("hmi.basic")
    dev.address    = cfg['config']['addr']
    dev.vendor_id  = "IHSEV"
    dev.product_id = "REST API"
    dev.version    = 0.1
    dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())

    engine.add_device(dev)
    monitor = Monitor(dev,filter_func=monitor_filter)
    engine.start()        
    green_let = Greenlet(xaal_loop, engine)
    green_let.start()

def xaal_loop(engine):
    """ xAAL Engine Loop Greenlet"""
    while 1:
        engine.loop()


@get('/static/<filename:path>')
def send_static(filename):
    root = os.path.dirname(__file__)
    root = os.path.join(root,'static')
    return static_file(filename, root=root)

@get('/')
def goto_html():
    redirect('/static/index.html')

@get('/devices')
@get('/devices/')
def list_devices():
    """ Return the list of devices in JSON"""
    l = []
    for dev in monitor.devices:
        h = {'address':dev.address,'devtype':dev.devtype}
        l.append(h)
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(l,indent=4)


@get('/devices/<addr>')
def get_device(addr):
    """ Return the full description of a device """
    dev=monitor.devices.get_with_addr(addr)
    response.headers['Content-Type'] = 'application/json'

    if dev:
        res = {'address':dev.address,'devtype':dev.devtype}
        res.update({'attributes':dev.attributes})
        res.update({'description':dev.description})
    else:
        res = {'error':{'code':404,'message':'Unknow device'}}
        response.status=404
    return json.dumps(res,indent=4)


def run():
    """ start the xAAL stack & launch the HTTP stuff"""
    setup_xaal()
    app = default_app()
    debug(True)
    server = WSGIServer(("", 8080), app, handler_class=WebSocketHandler)
    server.serve_forever()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye...")
    
    
    
if __name__ == '__main__':
    main()
