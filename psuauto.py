from lwModbusTCP import PSU
import time

ps = PSU('192.168.1.200', False)

ps.setVandC(12.0, 0.15)

while True:
    ps.getStats()

    ps.setOutputState(False)

    time.sleep(3)
    
    ps.setOutputState(True)

    time.sleep(4)

     