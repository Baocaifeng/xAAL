
from __future__ import print_function

import xaal.lib
import logging
import platform
from . import HTU21D


PACKAGE_NAME = "xaal.htu21d"

logger = xaal.lib.tools.get_logger(PACKAGE_NAME,logging.DEBUG,"%s.log" % PACKAGE_NAME)

def build_dev(addr,devtype):
    dev            = xaal.lib.Device(devtype)
    dev.address    = addr
    dev.vendor_id  = "IHSEV"
    dev.version    = 0.1
    dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
    dev.url        = "https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor/overview"
    dev.product_id = "HTU21D/I2C"
    return dev
        

def smooth(attribute,value,gap):
    old = attribute.value
    if not old:
        attribute.value = value
        return
    
    if not (old - gap <= value <= old + gap):
        attribute.value = value


class GW:
    def __init__(self,engine):
        self.engine = engine
        self.setup()
        
    def setup(self):
        cfg = xaal.lib.tools.load_cfg_or_die(PACKAGE_NAME)['config']
        rate = float(cfg['refresh'])
        self.engine.add_timer(self.process,rate)

        dev = build_dev(cfg['thermometer'],"thermometer.basic")
        self.temp = dev.new_attribute("temperature")
        self.engine.add_device(dev)
        
        dev = build_dev(cfg['hygrometer'],"hygrometer.basic")
        self.hum = dev.new_attribute("humidity")
        self.engine.add_device(dev)

        self.sensor = HTU21D.HTU21D()
        
    def process(self):
        smooth(self.temp,round(self.sensor.read_temperature(),1),0.1)
        smooth(self.hum,round(self.sensor.read_humidity(),0),1)
    
def run():
    eng = xaal.lib.Engine()
    gw = GW(eng)
    eng.run()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye...")
        
if __name__ == '__main__':
    main()
