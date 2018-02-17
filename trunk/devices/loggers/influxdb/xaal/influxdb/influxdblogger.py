#!/usr/bin/python2
# -*- coding: utf-8 -*-

#
#  Copyright 2017 Pierre-Henri Horrein, IMT Atlantique
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

import time
from xaal.lib import Device,Engine,tools,config

import influxdb

PACKAGE_NAME = "xaal.influxdb"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

class InfluxDBLogger:
    def __init__(self,engine):
        self.eng = engine
        # change xAAL call flow
        self.eng.add_rx_handler(self.parse_msg)
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)['config']
        self.setup()

    def setup(self):
        cfg = self.cfg

        client = influxdb.InfluxDBClient(
                host=cfg['host'],
                port=int(cfg['port']),
                username=cfg['user'],
                password=cfg['password'],
                database=cfg['database'],
                ssl=(cfg['ssl'] == "true"))
        self.influxdb = client

        dev = Device("logger.basic")
        dev.address    = self.cfg['addr']
        dev.vendor_id  = "IHSEV"
        dev.product_id = "InfluxDB Logger"
        dev.url        = "https://www.influxdata.com"
        dev.version    = 0.1
        dev.info  = "%s@%s:%s" % (cfg['database'],cfg['host'],cfg['port'])
        self.eng.add_device(dev)


    def parse_msg(self,msg):
        retry = 0
        done = False
        if msg.is_attributes_change() :
            data_points = []
            for k in msg.body:
                data_points.append({
                        "measurement": msg.source+"/"+k,
                        "fields": {
                            "value": msg.body[k]
                            },
                        }
                )
                logger.info("%s: %s/%s -> %s" %
                        (msg.timestamp,
                         msg.source,
                         k,
                         msg.body[k]
                            ))
            while not done: 
                try: 
                    self.influxdb.write_points(data_points,time_precision='s')
                    done = True
                except:
                    logger.warning("Exception when writing points, tries: " % retry)
                    if retry == 3:
                        logger.error("Message not logged, exceeded max retries")
                        done = True
                    retry+=1

def run():
    eng = Engine()    
    log = InfluxDBLogger(eng)
    eng.run()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye..")


if __name__ == '__main__':
    main()
