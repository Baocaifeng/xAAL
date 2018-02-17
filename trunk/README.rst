
Install
~~~~~~~
Right now, there is no public release (pip based) of xAAL Python binding. So
you have to install things from SVN or archive.

If you can use virtualenv (recommended). Python 3 version isn't mandatory but
highly recommended (some parts haven't be tested with Python 2 since a while).

First build a virtualenv :
$ virtualenv3 xaal_env
$ source xaal_env/bin/activate

Every time, you want to use the binding, you must source the activate script.

Download source files from SVN:
$ svn checkout https://redmine.telecom-bretagne.eu/svn/xaal/code/Python/trunk/ xaal_svn

First, install the xaal.lib package:
$ cd xaal_svn/libs/lib/
$ python setup.py develop

Install the monitor lib (needed for Dashboard, REST API..)
$ cd xaal_svn/libs/monitor/
$ python setup.py develop

Install the tools
$ cd xaal_svn/apps/tools
$ python setup.py develop

You can use the python setup.py install instead of develop, but modification
to source files, won't be applied, you have to re-install it. Right now develop,
is the better option. 

Create the configuration files in your home directory:
$ mkdir ~/.xaal/
$ cp xaal_svn/libs/lib/xaal.ini.sample ~/.xaal/xaal.ini
$ xaal-keygen

xaal-keygen will compute an key for a given passphrase. Edit the xaal.ini
file according to your needs.

"""
cassiel@dell:~/xAAL/trunk/libs/lib$ xaal-keygen
Please set key in config file [/home/cassiel/.xaal/xaal.ini]
Please enter your passphrase: baocaifeng
Cut & Paste this key in your xAAL config-file
key=06e98632d029e53450c58c29571f9d6aa92018e43ef6de218ef46b2f22cf599a
"""

Test
~~~~
First, you can launch a message dumper with this tools
$ xaal-dumper
$ or xaal-tail 

To start an fake lamp,
$ cd xaal_svn/devices/test/DummyDevices/
$ python lamp.py

To search for devices, you can use:
$ xaal-isalive
$ xaal-info xxxxxxxxxxxxxx <- uuid
$ xaal-walker 


Notes
~~~~~
- If you use xAAL on multiple hosts, take care of the system clock. xAAL use
  date/time to cypher the messages. If clocks differs, you will receive an error
  message about a "replay attack". In production, NTP is your best friend. A window
  of 1 minutes is accepted, but no more. 


Questions
~~~~~~~~~
- Python terminated by signal SIGSEGV: You probably forgot to setup the key in
  config file.

- Configuration files are hard to read / edit. Why don't you use YAML or XXML
  for config ?

  First, we need something that support nested config so we can
  not use ConfigParser. Next, we tested severals YAML packages, but they are
  really slow to import. We want xAAL stack to load as fast as possible, and
  importing big packages (like PyYAML) take around 0.5 sec on a Raspy. This
  is way too much for a simple command-line tools like xaal-info for example.
  We want to provide a better user experience.
  
