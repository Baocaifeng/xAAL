
from xaal.lib import Device


def build_dev(addr,devtype):
    dev            = Device(devtype)
    dev.address    = addr
    dev.vendor_id  = "DIY Wireless Bug"
    dev.url        = "http://dwb.ilhost.fr/"
    dev.version    = 0.3
    return dev
