
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pydispatch import dispatcher
import sys
import time


device="/dev/ttyACM0"
#device="/dev/ttyUSB0"
network = None

def connected():
    print("Connecting..")

def ready():
    print("Ready")

def disconnected():
    print("Disconnected")

def node_update(network, node):
    print('signal : Node update : {}.'.format(node))

def value_update(network, node, value):
    print('signal : Value update : {}.'.format(value))


def dump_device(node_id):
    zdev = network.nodes[node_id]
    print(zdev.product_name)
    for k in zdev.values:
        value = zdev.values[k]
        print("%s %s" % (value.label,value.data))
    
    

options = ZWaveOption(device)
options.set_console_output(False)
options.lock()

network = ZWaveNetwork(options, autostart=False)
network.start()

dispatcher.connect(connected, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(disconnected, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
dispatcher.connect(node_update, ZWaveNetwork.SIGNAL_NODE)
dispatcher.connect(value_update, ZWaveNetwork.SIGNAL_VALUE)


for i in range(0,90):
    if network.state>=network.STATE_READY:
        print("***** Network is ready")
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

import pdb;pdb.set_trace()


