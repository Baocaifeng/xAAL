from __future__ import print_function

from gevent import monkey; monkey.patch_all()
import gevent
import platform

from xaal.lib import tools,Engine,Device

from bugone import bugnet,connector
from .nodes import *


PACKAGE_NAME = "xaal.bugone"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

class GW(gevent.Greenlet):
    def __init__(self,engine):
        gevent.Greenlet.__init__(self)
        self.engine = engine
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)
        self.setup_connector()
        self.setup_nodes()
        self.setup_gw()
        
    def setup_connector(self):
        """ create the bugnet connector"""
        cn = None
        cfg = self.cfg['config']
        
        if cfg['type'] == 'tcpmux':
            cn = connector.TCPMux(cfg['host'])
        if cfg['type'] == 'serial':
            cn = connector.Serial(cfg['port'])

        if cn:
            self.bugnet = bugnet.BugNet(cn)
        else:
            logger.warn("Error in config section")
            
        
    def setup_nodes(self):
        """ load nodes from config file"""
        self.nodes = {}
        cfg = self.cfg['nodes']

        # creating nodes from config
        for k in cfg:
            node = None
            if cfg[k]['type'] == 'temp1':
                node = temp1.Node(k,cfg[k])
            if cfg[k]['type'] == 'mini-shield1':
                node = minishield1.Node(k,cfg[k])
            if node:
                self.nodes.update({int(k):node})
                self.engine.add_devices(node.get_devices())

    def setup_gw(self):
        # last step build the GW device
        gw            = Device("gateway.basic")
        gw.address    = self.cfg['config']['addr']
        gw.vendor_id  = "DIY Wireless Bug"
        gw.product_id = "bugOne Gateway"
        gw.version    = 0.3
        gw.url        = "http://dwb.ilhost.fr/"
        gw.info       = "%s@%s" % (PACKAGE_NAME,platform.node())

        emb = gw.new_attribute('embedded',[])
        for node in self.nodes.values():
            for dev in node.get_devices():
                emb.value.append(dev.address)
        self.engine.add_device(gw)

    def _run(self):
        """ receive pkt and foward it to right node"""
        while 1:
            pkt = self.bugnet.receive()
            print(pkt)            
            if pkt and pkt.src in self.nodes.keys():
                self.nodes[pkt.src].parse(pkt)
            
        
def run():
    eng = Engine()
    net = GW.spawn(eng)
    eng.run()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye...")
        
if __name__ == '__main__':
    main()
