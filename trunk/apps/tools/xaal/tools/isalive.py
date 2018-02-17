# -*- coding: utf-8 -*-

#
#  Copyright 2014 Jérôme Kerdreux, Telecom Bretagne.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from xaal.lib import Engine, Device, tools, config

import sys
import time

logger = tools.get_logger("isalive",'DEBUG')
class Scanner:

    def __init__(self,engine):
        self.eng = engine
        # new fake device
        self.addr = tools.get_random_uuid()
        self.dev = Device("cli.experimental",self.addr)
        self.eng.add_device(self.dev)
        self.eng.add_rx_handler(self.parse_answer)

    def query(self,devtype):
        self.devtype = devtype
        self.seen = []

        print("[%s] Sending xAAL isAlive [%s]" % (self.addr,self.devtype))
        self.eng.send_isAlive(self.dev,[self.devtype,])

        print("="*70)
        self.loop()
        print("="*70)

    def loop(self):
        t0 = time.time()
        while 1:
            self.eng.loop()
            if time.time() > (t0 + 1):
                break

    def parse_answer(self,msg):
        if (msg.is_notify()):
            if msg.is_alive():
                # hidding myself
                if msg.source == self.addr:
                    return
                #it is really for us ?
                if self.devtype != 'any.any':
                    if msg.devtype != self.devtype:
                        return
                # already seen this
                if msg.source in self.seen:
                    return
                # everything is Ok :)
                print("%s : %s" % (msg.source,msg.devtype))
                self.seen.append(msg.source)



def run():
    """ run the isalive scanner from cmdline"""
    eng = Engine()
    scan = Scanner(eng)
    eng.start()
    devtype = 'any.any'
    if len(sys.argv) == 2:
        devtype = sys.argv[1]
    scan.query(devtype)


def search(engine,devtype='any.any'):
    """ send request and return list of xaal-addr"""
    scan = Scanner(engine)
    scan.query(devtype)
    return scan.seen

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye bye")

if __name__ == '__main__':
    main()
