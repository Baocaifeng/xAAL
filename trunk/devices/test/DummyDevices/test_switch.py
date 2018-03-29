
from xaal.lib import Device,Engine,tools
import sys
import time,random

logger = tools.get_logger("test_switch.py","DEBUG")

def main(addr):
    if addr == None:
        addr = tools.get_random_uuid()
    dev = Device("switch.basic",addr)
    dev.product_id = 'One Simple test of Switch'
    dev.url = 'http://www.acme.org'

    # attributes
    state = dev.new_attribute('state')

    dev.dump()

    # methods
    def on():
        state.value = True
        print("%s ON" % dev)

    def off():
        state.value = False
        print("%s OFF" %dev)

    dev.add_method('on',on)
    dev.add_method('off',off)

    eng = Engine()
    eng.add_device(dev)
    #eng.run()
    eng.start()


if __name__ =='__main__':
    try:
        addr = None
        if len(sys.argv) > 1:
            addr = sys.argv[-1]
        main(addr)
    except KeyboardInterrupt:
        pass
