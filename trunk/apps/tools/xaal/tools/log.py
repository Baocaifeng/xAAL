""" dumb script that display attributes change the xAAL bus"""

import xaal.lib
import time

def print_evt(msg):
    if msg.is_attributes_change():
        print("%s %s %s %s" % (time.ctime(),msg.source,msg.devtype,msg.body))


def main():
    try:
        eng = xaal.lib.Engine()
        eng.add_rx_handler(print_evt)
        eng.run()
    except KeyboardInterrupt:
        print("ByeBye..")

if __name__ == '__main__':
    main()
