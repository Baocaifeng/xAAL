
xaal.influxdb
========
xaal.influxdb is an InfluxDB logger for xAAL. It can either log all values seen
on the bus, or log specific devices. 

For a full description of the protocol check out http://xaal.tk



Dependencies
~~~~~~~~~~~~
xaal.lib depends on :
- ujson
- pysodium
- configobj

But ujson compiled by hand (with pip install ie), will lead in a slow startup.
I'm unable to know exactly why. Using package distribution is really recommended.
If you can't, simply use json in place.

