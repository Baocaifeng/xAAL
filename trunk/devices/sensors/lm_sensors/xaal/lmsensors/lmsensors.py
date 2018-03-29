
from __future__ import print_function

import xaal.lib
import logging
import sensors
import platform
import time

PACKAGE_NAME = "xaal.lmsensors"

REFRESH_RATE = 30  # default rate : every 30 sec

logger = xaal.lib.tools.get_logger(PACKAGE_NAME,logging.DEBUG,"%s.log" % PACKAGE_NAME)


class LMSensors:
    def __init__(self,engine):
        self.engine = engine
        self.data = {}
        self.load_config()
        self.load_sensors()
        
    def load_config(self):
        cfg = xaal.lib.tools.load_cfg_or_die(PACKAGE_NAME)
        rate = REFRESH_RATE
        if cfg['config'].has_key('refresh'):
            rate = int(cfg['config']['refresh'])
        self.engine.add_timer(self.process,rate)
        self.cfg = cfg

    def load_sensors(self):
        # build a temp hashmap to collect sensors id & address
        sensors.init()
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                if feature.label in self.cfg['sensors'].keys():
                    dev = xaal.lib.Device("thermometer.basic")
                    dev.address    = self.cfg['sensors'][feature.label]['addr']
                    dev.vendor_id  = "IHSEV"
                    dev.product_id = "LM_SENSOR"
                    dev.url        = "https://wiki.archlinux.org/index.php/Lm_sensors"
                    dev.info       = "%s/%s/%s" % (platform.node(),chip.adapter_name,feature.label)
                    dev.version    = 0.2
                    temp = dev.new_attribute("temperature")
                    name = "%s:%s" % (chip,feature.label)
                    self.data.update({name:temp})
                    self.engine.add_device(dev)
                    dev.dump()


    def process(self):
        """ loop of lmsensors and update the devices attributes"""
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                name = "%s:%s" % (chip,feature.label)
                if name in self.data.keys():
                    self.data[name].value = feature.get_value()
    
    
def run():
    eng = xaal.lib.Engine()
    lm_sensors = LMSensors(eng)
    eng.run()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye...")
        
if __name__ == '__main__':
    main()
