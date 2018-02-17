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


from xaal.lib import tools
from xaal.lib.core import Engine

logger = tools.get_logger("dumper",'DEBUG')

def display(msg):
    msg.dump()

def main():
    try:
        eng = Engine()
        eng.add_rx_handler(display)
        eng.run()
    except KeyboardInterrupt:
        print("Bye Bye")


if __name__ == '__main__':
    main()
