
from xaal.lib import Device,Engine,tools,config
import platform,time
import pyowm
from pyowm.exceptions import OWMError

PACKAGE_NAME = "xaal.owm"
logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

RATE = 300 # update every 5 min

def build_dev(dtype,addr):
    dev = Device(dtype)
    dev.address    = addr
    dev.vendor_id  = "IHSEV"
    dev.product_id = "OpenWeatherMap"
    dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
    dev.url        = "https://www.openweathermap.org"
    dev.version    = 0.2
    return dev

class GW:
    def __init__(self,engine):
        self.eng = engine
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)
        self.setup()

    def setup(self):
        """ create devices, register .."""
        cfg = self.cfg['config']
      
        attr = {} 
        
        # devices
        temp = build_dev("thermometer.basic",cfg['temperature'])
        attr['temperature'] = temp.new_attribute('temperature')
        
        hum = build_dev("hygrometer.basic",cfg['humidity'])
        attr['humidity'] = hum.new_attribute('humidity')

        press = build_dev("barometer.basic",cfg['pressure'])
        attr['pressure'] = press.new_attribute('pressure')

        self.attr = attr
        self.devs = [temp,hum,press]
        
        # gw 
        gw = build_dev("gateway.basic",cfg['addr'])
        emb = gw.new_attribute('embedded',[dev.address for dev in self.devs])
        self.eng.add_devices(self.devs + [gw,])
        
        self.eng.add_timer(self.update,RATE)
        self.owm = pyowm.OWM(cfg['api_key'])

    def update(self):
        try:
            self._update()
        except OWMError as e:
            logger.warn(e)

    def _update(self):
        place = self.cfg['config']['place']
        weather = self.owm.weather_at_place(place).get_weather()
        self.attr['temperature'].value  = round(weather.get_temperature(unit='celsius')['temp'],1)
        self.attr['pressure'].value     = weather.get_pressure()['press']            
        self.attr['humidity'].value     = weather.get_humidity()

            
def run():
    eng = Engine()    
    log = GW(eng)
    eng.run()
    

def main():
    try:
        run()
    except KeyboardInterrupt:
        print("Bye Bye..")


if __name__ == '__main__':
    main()
