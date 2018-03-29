#I am supposed you have the environment of xaal on your computer.
#if not, look at this reference:
# https://redmine-df.telecom-bretagne.eu/projects/projet_dev_s2_30/repository/entry/trunk/README.rst
# any problem of netatmo gateway, please contect: caifeng.bao@imt-atlantique.net


#first,create the configuration files in your home directory:
$cd /home/cassiel/xAAL/trunk/devices/weather/NetatmoWeatherStation

$cp xaal.netatmo.ini.sample  ~/.xaal/xaal.netatmo.ini
$gedit ~/.xaal/xaal.netatmo.ini

#configure your xaal.netatmo.ini file
#if you don't understand the parametres in this file,look at this reference:
# https://dev.netatmo.com/resources/technical/samplessdks/codesamples

#second, test your netatmo gatway
#before you start, you should make sure your netatmo weather station is connected to netatmo cloud
#that is to say, your netatmo weather station is working
#and your computer needs to be connected to the Internet

#lauch at the xaal monitor
$xaal-tail 0

#then, lauch at anther terminal
$cd /home/cassiel/xAAL/trunk/devices/weather/NetatmoWeatherStation/xaal/netatmo
$python3 gw.py

#you will get information like this:
#2018-03-29 03:26:40,844 - requests.packages.urllib3.connectionpool - INFO - Starting new HTTPS connection (1): api.netatmo.com
#2018-03-29 03:26:41,130 - requests.packages.urllib3.connectionpool - DEBUG - "POST /oauth2/token HTTP/1.1" 200 None
#Your access token is: 5a7b5176b4809d4dde8b58ca|8b632b6ab6a9ec4242a37a8641501193
#2018-03-29 03:26:41,144 - requests.packages.urllib3.connectionpool - INFO - Starting new HTTPS connection (1): api.netatmo.com
#2018-03-29 03:26:41,298 - requests.packages.urllib3.connectionpool - DEBUG - "POST /api/getstationsdata?device_id=70%3Aee%3A50%3A1f%3A56%3A60&access_token=5a7b5176b4809d4dde8b58ca%7C8b632b6ab6a9ec4242a37a8641501193 HTTP/1.1" 200 None
#2018-03-29 03:26:41,312 - xaal.lib.network - INFO - Connecting to 224.0.29.200:1235
#2018-03-29 03:26:41,347 - requests.packages.urllib3.connectionpool - INFO - Starting new HTTPS connection (1): api.netatmo.com
#2018-03-29 03:26:41,536 - requests.packages.urllib3.connectionpool - DEBUG - "POST /oauth2/token HTTP/1.1" 200 None
#Your access token is: 5a7b5176b4809d4dde8b58ca|8b632b6ab6a9ec4242a37a8641501193
#2018-03-29 03:26:41,542 - requests.packages.urllib3.connectionpool - INFO - Starting new HTTPS connection (1): api.netatmo.com
#2018-03-29 03:26:41,697 - requests.packages.urllib3.connectionpool - DEBUG - "POST /api/getstationsdata?device_id=70%3Aee%3A50%3A1f%3A56%3A60&access_token=5a7b5176b4809d4dde8b58ca%7C8b632b6ab6a9ec4242a37a8641501193 HTTP/1.1" 200 None
#2018-03-29 03:26:41,700 - xaal.lib.devices - DEBUG - Attr change temperature=22.2
#2018-03-29 03:26:41,700 - xaal.lib.devices - DEBUG - Attr change humidity=51
#2018-03-29 03:26:41,700 - xaal.lib.devices - DEBUG - Attr change pressure=1018.5
#2018-03-29 03:26:41,700 - xaal.lib.devices - DEBUG - Attr change co2=1193
#2018-03-29 03:26:41,700 - xaal.lib.devices - DEBUG - Attr change noise=38



#at the same time, you can see the action of xaal devices on monitor
#the output will like this:

#notify  => attributes 3b96553a-32f0-11e8-9ecf-e0db55fb413a (noise_detector.basic) []                 {'noise': 38}
#notify  => attributes 3b96553a-32f0-11e8-9ecf-e0db55fb413a (air_quality.basic   ) []                 {'co2': 1193}
#notify  => attributes 3b96553a-32f0-11e8-9ecf-e0db55fb413a (hygrometer.basic    ) []                 {'humidity': 51}
#notify  => attributes 3b96553a-32f0-11e8-9ecf-e0db55fb413a (barometer.basic     ) []                 {'pressure': 1018.5}
#notify  => attributes 3b96553a-32f0-11e8-9ecf-e0db55fb413a (thermometer.basic   ) []                 {'temperature': 22.2}


#and also, you can do this:
$ xaal-isalive

#you will recieve this information:
#2018-03-29 04:21:17,387 - xaal.lib.network - INFO - Connecting to 224.0.29.200:1235
#[dc950dda-32f7-11e8-9ecf-e0db55fb413a] Sending xAAL isAlive [any.any]
#======================================================================
#d983ae76-32f7-11e8-9ecf-e0db55fb413a : thermometer.basic
#d983ae77-32f7-11e8-9ecf-e0db55fb413a : hygrometer.basic
#d983ae78-32f7-11e8-9ecf-e0db55fb413a : barometer.basic
#d983ae79-32f7-11e8-9ecf-e0db55fb413a : air_quality.basic
#d983ae7a-32f7-11e8-9ecf-e0db55fb413a : noise_detector.basic
#d983ae7b-32f7-11e8-9ecf-e0db55fb413a : gateway.basic
======================================================================
