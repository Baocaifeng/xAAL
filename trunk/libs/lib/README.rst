
xaal.lib
========
xaal.lib is the official python stack to developp home-automation devices
and gateways with the xAAL protocol.


For a full description of the protocol check out
http://recherche.imt-atlantique.fr/xaal/


Dependencies
~~~~~~~~~~~~
xaal.lib depends on :
- ujson
- pysodium
- configobj

But ujson compiled by hand (with pip install ie), will lead in a slow startup.
I'm unable to know exactly why. Using package distribution is really recommended.
If you can't, simply use json in place.

