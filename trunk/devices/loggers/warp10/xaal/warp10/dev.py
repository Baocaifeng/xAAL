
from xaal.lib import Device,Engine,tools,config

import sys
import platform
import urllib3

PACKAGE_NAME = "xaal.warp10"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

class WARP10Logger:
    def __init__(self,engine):
        self.eng = engine
        # change xAAL call flow
        self.eng.add_rx_handler(self.parse_msg)
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)['config']
        self.setup()

    def setup(self):
        dev = Device("logger.basic")
        dev.address    = self.cfg['addr']
        dev.vendor_id  = "IHSEV"
        dev.product_id = "WARP10 Logger"
        dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
        self.eng.add_device(dev)
        self.http = urllib3.PoolManager()

    def parse_msg(self,msg):
        if msg.is_attributes_change():
            base = self.cfg['topic']
            code = ''
            for k in msg.body:
                name = '%s.%s' % (base,k)
                tags  = '{devid=%s}' % msg.source
                value = msg.body[k]
                code = code +"// %s%s %s\n" % (name,tags,value)
            rsp = self.http.request('POST', self.cfg['url'],headers={'X-Warp10-Token':self.cfg['token']},body=code,retries=15)


def run():
    eng = Engine()
    log = WARP10Logger(eng)
    eng.run()


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye..")


if __name__ == '__main__':
    main()
