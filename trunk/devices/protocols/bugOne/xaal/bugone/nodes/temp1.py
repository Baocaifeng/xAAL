

from xaal.lib import Device, Attribute
from .default import build_dev

           

class Node(object):
    def __init__(self,ID,cfg):
        base_addr = cfg["base_addr"][:-1]
        group = cfg["group"]

        attr = {}
        
        # first device = bangap
        bg = build_dev(base_addr+'1',"voltage.basic")
        bg.info = "bandgap"
        bg.hw_id = "%s.1" % ID
        attr["voltage"] = bg.new_attribute("voltage")
        
        # temp sensor
        temp = build_dev(base_addr+'2',"thermometer.basic")
        temp.info = "DS18B20"
        temp.hw_id = "%s.2" % ID
        attr["temperature"] = temp.new_attribute("temperature")

        self.devs = [bg,temp]
        self.attr = attr
        
        for dev in self.devs:
            dev.product_id = 'temp1'
            dev.group_id = group

    def parse(self,pkt):
        try:
            self.attr["voltage"].value     = pkt.values[0][2]/100.0
            self.attr["temperature"].value = pkt.values[1][2]/10.0
        except IndexError:
            pass
    
    def get_devices(self):
        return self.devs
