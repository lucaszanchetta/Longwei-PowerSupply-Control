#!/usr/bin/env python3
from serial import *
import minimalmodbus
import time


instrument = minimalmodbus.Instrument('/dev/tty.usbserial-AR0K4G5P', 1, debug= True)  # port name, slave address (in decimal)

instrument.serial.port                     # this is the serial port name
instrument.serial.baudrate = 9600         # Baud
instrument.serial.bytesize = 8
# instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.05

## Read temperature (PV = ProcessValue) ##
#temperature = instrument.read_register(0x1004, 0)  # Registernumber, number of decimals

while (True):
    values = instrument.read_registers(0x1000, 6, 3)

    setVolage = values[0] / 100
    setCurrent = values[1] / 1000
    v = values[2] / 100
    a = values[3] / 1000
    state = values[5]

    '''
    if (a < 0.23):
        instrument.write_register(0x1006, 0, 0, 6)
    '''
    
    print('V: %fV, A: %fA, State %d' % (v, a, state))
    time.sleep(5)
