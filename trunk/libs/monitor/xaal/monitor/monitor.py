
import time,random

import logging
logger = logging.getLogger(__name__)

HIDDEN_ATTRIBUTES = ['busAddr','busPort','hops']

class Device:
    def __init__(self, addr, devtype, version):
        self.address = addr
        self.devtype = devtype
        self.version = version

        self.attributes = {}
        self.description = {}
        self.db = {}

        self.last_alive = int(time.time())
        self.next_alive = 0
        self.refresh = 0

        print("Adding %s - %s" % (addr, devtype))

    def update_attributes(self, data):
        """ rude update attributes. Return true if updated"""
        keys = list(data.keys())
        change = False
        for k in keys:
            if k in HIDDEN_ATTRIBUTES:
                data.pop(k)
        # really no the best comparaison, but we just need a flag
        if self.attributes == data:
            return False
        self.attributes.update(data)
        return True

    def update_description(self, data):
        self.description.update(data)

    def update_db(self,data):
        self.db.update(data)

    def alive(self,value):
        self.last_alive = int(time.time())
        self.next_alive = self.last_alive + value

    def get_kv(self,key):
        try:
            return self.db[key]
        except KeyError:
            return None

    """
    def __cmp__(self,other):
        if (self.devtype == other.devtype):
            if self.address > other.address:
                return 1
            else:
                return -1
        if (self.devtype > other.devtype):
            return 1
        if (self.devtype < other.devtype):
            return -1
        return 0
    """

    def dump(self):
        print("*** %s %s **" % (self.address,self.devtype))
        print("    Description : %s" % self.description)
        print("    Attributes : %s" % self.attributes)
        print()



class Devices:
    def __init__(self):
        self.__devs = {}
        self.__list_cache = None

    def add(self,addr,devtype,version):
        dev = Device(addr,devtype,version)
        self.__devs.update({addr : dev})
        self.__list_cache = None


    def get(self):
        if not self.__list_cache:
            print("Refresh cache")
            res = list(self.__devs.values())
            res.sort(key = lambda d: d.devtype)
            self.__list_cache = res
        return self.__list_cache

    def get_with_addr(self, addr):
        try:
            return self.__devs[addr]
        except KeyError:
            return None

    def get_with_devtype(self,devtype):
        r = []
        for d in self.get():
            if d.devtype == devtype:
                r.append(d)
        return r

    def get_with_key(self,key):
        r = []
        for d in self.get():
            if key in d.db:
                r.append(d)
        return r

    def get_with_key_value(self,key,value):
        r = []
        for d in self.get():
            if (key in d.db) and (d.db[key]==value):
                r.append(d)
        return r

    def fetch_one_kv(self,key,value):
        r = self.get_with_key_value(key,value)
        try:
            return r[0]
        except IndexError:
            return None
    
    def get_devtypes(self):
        """ return the list of distinct devtypes"""
        l = []
        for dev in self.__devs.values():
            if dev.devtype not in l:
                l.append(dev.devtype)
        l.sort()
        return l

    def __len__(self):
        return len(self.__devs)

    def __getitem__(self,idx):
        if isinstance(idx, str):
            return self.__devs[idx]
        return self.get()[idx]

    def __repr__(self):
        return str(self.get())

    def __contains__(self,key):
        return key in self.__devs

    def auto_wash(self):
        now = int(time.time())
        for dev in self.get():
            if dev.next_alive < now:
                logger.info("Auto Washing %s" % dev.address)
                del self.__devs[dev.address]
                self.__list_cache = None

    def display(self):
        for d in self.get():
            print("%s %s" % (d.address,d.devtype))


class Monitor:
    """
    class xAAL Monitor:
    use this class to monitor a xAAL network
    """
    def __init__(self,device,filter_func=None,db_server=None):
        self.dev = device
        self.engine = device.engine
        self.db_server = db_server
        
        self.devices = Devices()
        self.filter = filter_func
        self.subscribers = []
        self.engine.add_rx_handler(self.parse_msg)
        self.engine.add_timer(self.auto_wash, 10)
        self.engine.add_timer(self.send_isalive, 180)
        self.engine.add_timer(self.refresh_devices, 5)

    def parse_msg(self, msg):
        # do nothing for some msg
        if (self.filter!=None) and self.filter(msg)==False:
            return

        if msg.source not in self.devices:
            self.add_device(msg)

        dev = self.devices.get_with_addr(msg.source)

        if msg.is_alive():
            dev.alive(msg.body['timeout'])

        elif msg.is_attributes_change() or msg.is_get_attribute_reply():
            r = dev.update_attributes(msg.body)
            if r:
                self.notify('ATTRIBUTE_CHANGE',dev)

        elif msg.is_get_description_reply():
            dev.update_description(msg.body)

        elif self.is_reply_metadb(msg):
            addr = msg.body['device']
            target = self.devices.get_with_addr(addr)
            if target:
                target.db = msg.body['map']

        elif self.is_udpdate_metadb(msg):
            addr = msg.body['device']
            target = self.devices.get_with_addr(addr)
            if target:
                target.update_db(msg.body['map'])
        
    def subscribe(self,func):
        self.subscribers.append(func)

    def notify(self,ev_type,device):
        for s in self.subscribers:
            s(ev_type,device)

    def add_device(self,msg):
        self.devices.add(msg.source,msg.devtype,msg.version)

    def send_isalive(self):
        self.engine.send_isAlive(self.dev, "any.any")

    def auto_wash(self):
        """call the Auto-wash on devices List"""
        self.devices.auto_wash()

    def refresh_devices(self):
        now = int(time.time())
        for dev in self.devices:
            if dev.refresh + 180 < now:
                self.request_metadb(dev.address)
                self.engine.send_get_attributes(self.dev,[dev.address,])
                self.engine.send_get_description(self.dev,[dev.address,])
                # to avoid bulk send, we introduce this salt in refresh
                dev.refresh = now - random.randint(0,20)

    def request_metadb(self,addr):
        self.db_server = 'd28fbc27-190f-4ee5-815a-fe05233400a1'
        self.engine.send_request(self.dev,[self.db_server,],'getKeysValues',{'device':addr})
        
    def is_reply_metadb(self,msg):
        if msg.msgtype == 'reply' and msg.action == 'getKeysValues':
            return True

    def is_udpdate_metadb(self,msg):
        if msg.msgtype == 'notify' and msg.action == 'keysValuesChanged':
            return True
        return False
