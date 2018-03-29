from xaal.lib import Device,Engine,tools,config
import platform
import requests
import sys



PACKAGE_NAME = "xaal.netatmo"

logger = tools.get_logger(PACKAGE_NAME,'DEBUG')

RATE = 300 # update every 5 min


class GW:
    def __init__(self,engine):
        self.eng = engine
        self.cfg = tools.load_cfg_or_die(PACKAGE_NAME)
        self.setup()


    def setup(self):
        pass
        #devices
        attr = {}
        addr1 = tools.get_random_uuid()
        temp = build_dev("thermometer.basic",addr1)
        attr['temperature'] = temp.new_attribute('temperature')
        addr2 = tools.get_random_uuid()
        hum = build_dev("hygrometer.basic",addr2)
        attr['humidity'] = hum.new_attribute('humidity')
        addr3 = tools.get_random_uuid()
        press = build_dev("barometer.basic",addr3)
        attr['pressure'] = press.new_attribute('pressure')
        addr4 = tools.get_random_uuid()
        co = build_dev("air_quality.basic",addr4)
        attr['co2'] = co.new_attribute('co2')
        addr5 = tools.get_random_uuid()
        no = build_dev("noise_detector.basic",addr5)
        attr['noise'] = no.new_attribute('noise')

        self.attr = attr
        self.devs = [temp,hum,press,co,no]


        # gw
        addr = tools.get_random_uuid()
        gw = build_dev("gateway.basic",addr)
        emb = gw.new_attribute('embedded',[dev.address for dev in self.devs])
        self.eng.add_devices(self.devs + [gw])
        self.eng.add_timer(self.update,RATE)

    def connect(self):
        pass
        """ connect to netatmo cloud .."""
        ##read config
        cfg = self.cfg['config']
        payload = {
            'grant_type'      :   cfg['grant_type'],
            'client_id'       :   cfg['client_id'],
            'client_secret'   :   cfg['client_secret'],
            'password'        :   cfg['password'],
            'username'        :   cfg['username'],
            'scope'           :   cfg['scope']
        }

        try:
            response = requests.post("https://api.netatmo.com/oauth2/token", data=payload)
            response.raise_for_status()
            access_token=response.json()["access_token"]
            print("Your access token is:", access_token)
            return access_token

        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)


    def update(self):
        self.__readweatherstation()
        print("update")

    def __readweatherstation(self):
        cfg = self.cfg['config']
        params = {
            'access_token': self.connect() ,
            'device_id': cfg['device_id']
        }

        try:
            response = requests.post("https://api.netatmo.com/api/getstationsdata", params=params)
            response.raise_for_status()
            data = response.json()["body"]["devices"][0]["dashboard_data"] # 16 items
            temperature=data["Temperature"]
            humidity=data["Humidity"]
            pressure=data["Pressure"]
            co2=data["CO2"]
            noise=data["Noise"]
        except requests.exceptions.HTTPError as error:
            print(error.response.status_code, error.response.text)

        self.attr['temperature'].value  = temperature
        self.attr['humidity'].value     = humidity
        self.attr['pressure'].value     = pressure
        self.attr['co2'].value     = co2
        self.attr['noise'].value     = noise


def build_dev(dtype,addr):
    dev = Device(dtype)
    dev.address    = addr
    dev.vendor_id  = "NETATMO"
    dev.product_id = "NetatmoWeatherStation"
    dev.info       = "%s@%s" % (PACKAGE_NAME,platform.node())
    dev.url        = "https://dev.netatmo.com/"
    dev.version    = 0.1
    return dev

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