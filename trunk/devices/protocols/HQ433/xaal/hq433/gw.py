from __future__ import print_function

from xaal.lib import tools,Engine,Device

import platform
import serial

PACKAGE_NAME = "xaal.hq433"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')


def new_dev(gw,key,channel,addr,dtype):
    """ create e new xAAL device """
    dev = None
    if dtype=='lamp':
        dev = Device("lamp.basic",addr)
        dev.product_id = "Lamp on HQ Product RF433 power relay"
        var = dev.new_attribute('light')
    else:
        dev = Device("powerrelay.basic",addr)
        dev.product_id = "HQ Product RF433 power relay"
        var = dev.new_attribute('power')        

    dev.vendor_id = "JKX"
    dev.hw_id = '%s%s' % (key,channel)
    dev.version = 0.2
    dev.info = "%s@%s" % (PACKAGE_NAME,platform.node())
                
    # methods 
    def on():
        if gw.switch_relay('ON',key,channel):
            var.value = True    
        
    def off():
        if gw.switch_relay('OFF',key,channel):
            var.value = False

    dev.add_method('on',on)
    dev.add_method('off',off)
    return dev



class GW(object):
    def __init__(self,engine):
        self.engine = engine
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)
        self.setup()
        
    def setup(self):
        """ connect to serial port, and load configuration file"""
        # connect to serial port
        port = self.cfg['config']['port']
        self.ser = serial.Serial(port,19200,timeout=0.5)
        
        # load devices from 
        devices = [] 
        relays = self.cfg['relays']
        for k in relays:
            dev = new_dev(self,k[0],k[1],relays[k]['addr'],relays[k]['type'])
            devices.append(dev)
        self.engine.add_devices(devices)

        # last step build the GW device
        gw            = Device("gateway.basic")
        gw.address    = self.cfg['config']['addr']
        gw.vendor_id  = "JKX"
        gw.product_id = "HQ Product RF433 Gateway"
        gw.version    = 0.1
        gw.info       = "%s@%s" % (PACKAGE_NAME,platform.node())

        emb = gw.new_attribute('embedded',[])
        emb.value = [dev.address for dev in devices]
        self.engine.add_device(gw)

    def switch_relay(self,cmd,key,channel):
        """ turn on & off relay via serial arduino"""
        r = '%s %s %s\r\n' % (cmd,key,channel)
        self.ser.write(r.encode())
        line = self.ser.readline()
        print(line,end='')
        return True


def run():
    eng = Engine()
    gw = GW(eng)
    eng.run()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye...")
        
if __name__ == '__main__':
    main()
