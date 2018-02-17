
from xaal.lib import tools,Engine,Device
from xaal.monitor import Monitor

import platform

PACKAGE_NAME = "xaal.monitorexample"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')


def display_event(event,dev):
    print("MonitorExample: %s %s %s" %(event, dev.address, dev.attributes))

def monitor_example(engine):
    # load config
    cfg = tools.load_cfg_or_die(PACKAGE_NAME)
    # create a device & register it
    dev            = Device("hmi.basic")
    dev.address    = cfg['config']['addr']
    dev.vendor_id  = "IHSEV"
    dev.product_id = "Monitor Example"
    dev.version    = 0.1
    dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
    engine.add_device(dev)
    # start the monitoring
    mon = Monitor(dev)
    mon.subscribe(display_event)
    return mon

def run():
    print("Monitor test")
    eng = Engine()
    mon = monitor_example(eng)
    try:
        eng.run()
    except KeyboardInterrupt:
        import pdb;pdb.set_trace()

if __name__ == '__main__':
    run()
    
