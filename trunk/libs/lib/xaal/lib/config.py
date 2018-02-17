
# Default configuration
import os
import sys
import binascii
from configobj import ConfigObj

self = sys.modules[__name__]

# Default settings
DEF_ADDR = '224.0.29.200'   # mcast address
DEF_PORT = 1235             # mcast port
DEF_HOPS = 10               # mcast hop
DEF_ALIVE_TIMER = 100       # Time between two alive msg
DEF_CIPHER_WINDOW = 60 * 2  # Time Window in seconds to avoid replay attacks



# TBD : Move this stuff
STACK_VERSION = '0.5'
XAAL_BCAST_ADDR = '00000000-0000-0000-0000-000000000000'


if 'XAAL_CONF_DIR' in os.environ:
    self.conf_dir = os.environ['XAAL_CONF_DIR']
else:
    self.conf_dir = os.path.expanduser("~") + '/.xaal'


def load_config(name='xaal.ini'):
    filename = os.path.join(self.conf_dir, name)
    if not os.path.isfile(filename):
        print("Unable to load xAAL config file [%s]" % filename)
        sys.exit(-1)

    cfg = ConfigObj(filename)
    self.address       = cfg.get('address',DEF_ADDR)
    self.port          = int(cfg.get('port',DEF_PORT))
    self.hops          = int(cfg.get('hops',DEF_HOPS))
    self.alive_timer   = int(cfg.get('alive_timer',DEF_ALIVE_TIMER))
    self.cipher_window = int(cfg.get('ciper_window',DEF_CIPHER_WINDOW))
    key = cfg.get('key',None)

    if key:
        self.key = binascii.unhexlify(key.encode('utf-8'))
    else:
        print("Please set key in config file [%s]" % filename)
        self.key = None

load_config()
