
import paho.mqtt.client as mqtt
from xaal.lib import Device,Engine,tools,config

import sys


# Hardcoded nickname, because metadata server is not ready

NICKNAME= { '2f31c921-02b2-4097-bfae-5753dde2cd40' : 'salon',
            '2f31c921-03b2-4097-bfae-5753dde2cd40' : 'salon',
            '2f31c922-02b2-4097-bfae-5753dde2cd40' : 'bureau',
            '2f31c922-03b2-4097-bfae-5753dde2cd40' : 'bureau',
            '2f31c933-02b2-4097-bfae-5753dde2cd40' : 'chambre',
            'c7fed8ba-1ead-11e7-8249-82ed25e6aaaa' : 'test',
            '5fcc6ad0-804d-49cb-b66c-e877f2374905' : 'exterieur',
            '5fcc6ad1-804d-49cb-b66c-e877f2374905' : 'exterieur',
}


PACKAGE_NAME = "xaal.mqttlogger"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

class MQTTLogger:
    def __init__(self,engine):
        self.eng = engine
        # change xAAL call flow
        self.eng.add_rx_handler(self.parse_msg)
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)['config']
        self.setup()

    def setup(self):
        """ connect to mqtt server & register xaal dev"""
        cfg = self.cfg
        client = mqtt.Client(client_id=cfg['client_id'], clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
        client.username_pw_set(cfg['username'],cfg['password'])
        client.connect(host=cfg['host'], port=int(cfg['port']), keepalive=60, bind_address="")
        client.loop_start()
        self.mqtt = client

        dev = Device("logger.basic")
        dev.address    = self.cfg['addr']
        dev.vendor_id  = "IHSEV"
        dev.product_id = "MQTT Logger"
        dev.info       = "%s@%s:%s" % (cfg['client_id'],cfg['host'],cfg['port'])
        self.eng.add_devices([dev,])


    def parse_msg(self,msg):
        if msg.is_attributes_change() :
            nick = self.get_nickname(msg.source)
            if nick:
                base = "%s/%s" % (self.cfg['topic'],nick)
                for k in msg.body:
                    topic = '%s/%s' % (base,k)
                    print("%s = %s" % (topic,msg.body[k]))
                    self.mqtt.publish(topic,payload=msg.body[k],qos=0,retain=True)

    def get_nickname(self,addr):
        """ return a nickname for a device """
        try:
            nick = NICKNAME[addr]
        except KeyError:
            nick = None
        return nick


def run():
    eng = Engine()
    log = MQTTLogger(eng)
    eng.run()


def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye..")


if __name__ == '__main__':
    main()
