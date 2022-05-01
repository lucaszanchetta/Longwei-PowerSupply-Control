from cgi import test
from serial import *
import minimalmodbus
import time

class PSU:

    def __init__(self, serialPort, debug):

        self.ps = minimalmodbus.Instrument(serialPort, 1, debug=debug, close_port_after_each_call=False)  # port name, slave address (in decimal)
        self.ps.serial.baudrate = 9600
        self.ps.serial.timeout = 0.1
        self.ps.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.ps.serial.bytesize = 8
        self.ps.serial.stopbits = 1
        self.ps.mode = minimalmodbus.MODE_RTU


        self.values = self.ps.read_registers(0x1000, 6, 3)
        self.vSetPoint = 0
        self.aSetPoint = 0
        self.v = 0
        self.a = 0
        self.state = 0
        self.outputMode = 0

        print("Connecting to Power Supply")
        self.printStats()
        print("Connected to Power Supply via Serial!!!\n")
        

    def getStats(self):
        self.values = self.ps.read_registers(0x1000, 6, 3)
        self.vSetPoint = self.values[0] / 100
        self.aSetPoint = self.values[1] / 1000
        self.v = self.values[2] / 100
        self.a = self.values[3] / 1000
        self.state = self.values[4]
        self.outputMode = self.values[5]
        if self.state == 1:
            self.state = "ON"
        elif self.state == 0:
            self.state = "OFF"
        else:
            self.state = "???"

        if self.outputMode == 0:
            self.outputMode = 'CC'
        
        elif self.outputMode == 1:
            self.outputMode = 'CV'

        elif self.outputMode == 2:
            self.outputMode = 'OC'

        else:
            self.outputMode = '???'
        

    def setOutputState(self, val):
        self.ps.write_register(4102, val, 0 ,6)
        time.sleep(0.1)

    def setVoltage(self, voltage):
        if voltage > 0 and voltage <= 31:
            self.ps.write_register(4096, voltage, 2, 6)
            time.sleep(0.1)

    def setCurrent(self, current):
        if current > 0 and current <= 5.1:
            self.current = current * 10
            self.ps.write_register(4097, self.current, 2, 6)
            time.sleep(0.1)

    def setVandC(self, voltage, current):
        self.setVoltage(voltage)
        time.sleep(0.1)
        self.setCurrent(current)
        time.sleep(0.1)

    def getOutputState(self):
        return self.state

    def printStats(self):
        self.getStats()
        print("V Setpoint: %s | A Setpoint: %s | State: %s" % (self.vSetPoint, self.aSetPoint, self.state))
        print("Output Stats: ")
        print("V: %s | A: %s | Mode: %s" % (self.v, self.a, self.outputMode))

