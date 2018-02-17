
from xaal.lib import Engine,Device,tools
import platform
import copy
import atexit

PACKAGE_NAME = "xaal.metadb"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')


class MetaDB(object):
    def __init__(self,engine):
        self.engine = engine 
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)
        self.setup()
        self.dirty = False
        atexit.register(self.periodic_save)
        
    def setup(self):
        addr = self.cfg['config']['addr']
        dev            = Device("metadatadb.basic")
        dev.address    = addr
        dev.vendor_id  = "IHSEV"
        dev.product_id = "Metadata database"
        dev.version    = 0.1
        dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
        
        dev.add_method('getDevices',self.get_devices)
        dev.add_method('getKeysValues',self.get_keys_values)
        dev.add_method('getValue', self.get_value)
        dev.add_method('updateKeysValues', self.update_keys_values)
        dev.add_method('addKeysValues', self.add_keys_values)
        
        self.dev = dev
        self.engine.add_device(dev)
        self.engine.add_timer(self.periodic_save,60)

    def get_devices(self,_key=None,_value=None):
        devices = self.cfg['devices'] 
        result = devices.keys()

        # search for a given key=value and break
        if _key and _value:
            value = str(_value)
            temp = [] 
            for dev in result:
                if _key in devices[dev].keys():
                    if devices[dev][_key] == value:
                        temp.append(dev)
            return {'key':_key,'value' : _value, 'devices' : temp}
        
        # filter key
        if _key:
            for dev in copy.copy(result):
                #print("%s %s %s" % (dev,key,devices[dev].keys()))
                if _key not in devices[dev].keys():
                    result.remove(dev)

        # filter value
        if _value:
            value = str(_value)
            for dev in copy.copy(result):
                print("%s %s %s" % (dev,value,devices[dev].values()))
                if value not in devices[dev].values():
                    result.remove(dev)
        return {'key':_key,'value' : _value, 'devices' : result}

    def get_device(self,addr):
        devices = self.cfg['devices']
        try:
            return devices[addr]
        except KeyError:
            return None

    def get_keys_values(self,_device):
        dev = self.get_device(_device)
        if dev:
            return {'device':_device,'map' : dev}
        logger.info('Unknown device %s' % _device)

    def get_value(self,_device,_key):
        dev = self.get_device(_device)
        if not dev:
            logger.info('Unknown device %s' % _device)
            return 
        try:
            return {'device': _device, 'key':_key,'value':dev[_key]}
        except KeyError:
            logger.info('Unknown key %s for %s' % (_key,_device))

    def update_keys_values(self,_device,_map):
        dev = self.get_device(_device)
        updated = {}
        if dev:
            # if _map is empty, remove the device
            if _map == None:
                self.cfg['devices'].pop(_device)
                self.dirty = True
                return
            # loop throught the map 
            for k in _map:
                # remove item if empty
                if _map[k] == None:
                    dev.pop(k)
                    self.dirty = True
                else:
                    dev.update({k:_map[k]})
                    updated.update({k:_map[k]})
                    self.dirty = True
        else:
            self.cfg['devices'][_device]=_map
            updated = _map
            self.dirty = True

        if len(updated):
            body = {'device':_device,'map':updated}
            self.engine.send_notification(self.dev,'keysValuesChanged',body)

    def add_keys_values(self,_device,_map):
        dev = self.get_device(_device)
        updated = {}
        if dev:
            for k in _map:
                if k not in dev.keys():
                    dev.update({k:_map[k]})
                    updated.update({k:_map[k]})
                    self.dirty = True
        else:
            self.cfg['devices'][_device]=_map
            updated = _map
            self.dirty = True
            
        if len(updated):
            body = {'device':_device,'map':updated}
            self.engine.send_notification(self.dev,'keysValuesChanged',body)
            
    def periodic_save(self):
        if self.dirty:
            logger.info("Saving configuration file")
            self.cfg.write()
            self.dirty = False

def run():
    eng = Engine()    
    mdb = MetaDB(eng)
    eng.run()

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye..")
        
if __name__=='__main__':
    main()
