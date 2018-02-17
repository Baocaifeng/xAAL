# -*- coding: utf-8 -*-

#
#  Copyright 2014 Jérôme Colin, Jérôme Kerdreux, Telecom Bretagne.
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

from xaal.lib.core import Engine
from xaal.lib import tools

from .ansi2 import term
import sys

level = 0

FORMAT = '%-8.08s=> %-10.10s %-36.36s (%-20.20s) %-18.18s %-45.45s'

logger = tools.get_logger("tail",'DEBUG')

def reduceAddr(addr):
    return addr[:5] + '..' + addr[-5:]

def display(msg):
    term('yellow')
    targets = [reduceAddr(addr) for addr in msg.targets]
    res = FORMAT % (msg.msgtype,msg.action,msg.source,msg.devtype,targets,msg.body)

    if msg.is_request():
        if level > 2: return
        term('green')

    if msg.is_reply():
        if level > 1: return
        term('red')

    if msg.is_notify():
        if msg.is_alive():
            if level > 0: return
            term('grey')
        if msg.is_attributes_change():
            term('cyan')

    print(res)




def usage():
    print("%s : monitor xAAL network w/ tail format" % sys.argv[0])
    print("  usage : %s log-level" % sys.argv[0])
    print("    level=0 => display all messages")
    print("    level=1 => hide alive messages")
    print("    level=2 => hide reply messages")
    print("    level=3 => only display attributesChange")



def main():
    global level
    if len(sys.argv) == 2:
        level = int(sys.argv[1])

        eng = Engine()
        eng.add_rx_handler(display)

        eng.start()
        term('@@')
        print(FORMAT % ('msgType','action','source','devType','targets','body'))
        try:
            eng.run()
        except KeyboardInterrupt:
            pass
    else:
        usage()

if __name__ == '__main__':
    main()
