
import time,random,sys
from xaal.lib import Engine,Device,tools

target = sys.argv[-1] 
dev = Device("switch.basic",tools.get_random_uuid())

eng = Engine()
eng.start()

while 1:
    
    eng.send_request(dev,[target,],'dim',{'target':random.randint(0,100)})
    eng.loop()
    time.sleep(5)

    eng.send_request(dev,[target,],'on')
    print('ON')
    eng.loop()
    time.sleep(3)

    eng.send_request(dev,[target,],'off')
    print('OFF')
    eng.loop()
    time.sleep(3)
