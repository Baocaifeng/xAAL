
from xaal.lib import Device,Attribute



class OutputChannel(object):

    def __init__(self,ipx,channel,addr,state_name,group):
        dev = Device("changeme.basic",addr)
        dev.vendor_id  = "IHSEV"
        dev.version    = 0.1
        dev.hw_id = channel
        dev.group_id = group
        
        # attribute
        self.state = dev.new_attribute(state_name)
        
        # method 
        dev.add_method('on',self.on)
        dev.add_method('off',self.off)

        self.chan = channel
        self.ipx = ipx 
        self.dev = dev

    def on(self):
        self.ipx.relay_on(self.chan)
    
    def off(self):
        self.ipx.relay_off(self.chan)

def new_lamp(ipx,channel,addr,group):
    lamp = OutputChannel(ipx,channel,addr,'light',group)
    lamp.dev.devtype = 'lamp.basic'
    lamp.dev.product_id = 'IPX-800 Lamp'
    return lamp


def new_relay(ipx,channel,addr,group):
    relay = OutputChannel(ipx,channel,addr,'power',group)
    relay.dev.devtype = 'powerrelay.basic'
    relay.dev.product_id = 'IPX-800 Power Relay'
    return relay
