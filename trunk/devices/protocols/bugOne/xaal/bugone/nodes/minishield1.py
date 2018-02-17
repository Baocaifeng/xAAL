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
        temp.info = "SHT21/temp"
        temp.hw_id = "%s.2" % ID
        attr["temperature"] = temp.new_attribute("temperature")
        
        # hum sensor
        hum = build_dev(base_addr+'3',"hygrometer.basic")
        hum.info = "SHT21/rh"
        hum.hw_id = "%s.3" % ID
        attr["humidity"] = hum.new_attribute("humidity")

        self.devs = [bg,temp,hum]
        self.attr = attr
        for d in self.devs:
            d.product_id = 'minishield1'
            d.group_id = group

    def parse(self,pkt):
        try:
            self.attr["voltage"].value      = pkt.values[0][2]/100.0
            self.attr["temperature"].value  = pkt.values[1][2]/10.0
            self.attr["humidity"].value     = int(round(pkt.values[2][2]/10.0))
        except IndexError:
            pass
        
        
    def get_devices(self):
        return self.devs
