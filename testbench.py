from select import select
from lwModbus import PSU
import paho.mqtt.client as paho
import time
import random
import os

#Broker IP and port
broker="192.168.1.127"
port=1883

def on_publish(client,userdata,result):
    print("data published \n")
    pass

client1= paho.Client("testBench")
client1.on_publish = on_publish
client1.connect(broker,port)

myPSU = PSU('/dev/tty.usbserial-AR0K4G5P', False)

def setSafeAndOn():
    print("Setting Powersupply Parameters....")
    myPSU.setVandC(12.00, 0.350)
    time.sleep(0.5)
    print("Turning ON Powersupply")
    myPSU.setOutputState(1)

def relayTest():
    clear = os.system('clear')

    print("")
    print("########################################\n")
    print("RELAY TEST\n")
    print("     [1] Begin")
    print("     [b] to go back | [q] quit\n")

    confirm = input("Enter Selection: ")

    if confirm == 'q':
        exit()

    elif confirm == 'b':
        menu()

    elif confirm == '1':

        print("####     Begining Test     ####\n")
        print("Press ^c to stop at any time\n")

        setSafeAndOn()

        time.sleep(2)

        try:
            while (True):

                def relayRand():
                    flip = random.randint(0, 1)

                    if flip == 0:
                        state = "off"
                    elif flip == 1:
                        state = "on"

                    return state

                r = relayRand()
                ret= client1.publish("aqua/lights", r)
                time.sleep(1)
                print("")
                myPSU.printStats()
                print("")
                print("RELAY1: %s" % (r))

                r = relayRand()
                rt = random.randint(1,15)
                print("RELAY2 %s in %ds" % (r, rt))
                time.sleep(rt)
                ret= client1.publish("aqua/ato", relayRand())
                time.sleep(1)
                print("")
                myPSU.printStats()
                print("")
                print("RELAY2: %s" % (r))

                rt = random.randint(1,15)
                print("Sleeping for %ds" % (rt))
                print("")
                myPSU.printStats()
                print("\n")

                time.sleep(rt)

        except KeyboardInterrupt:
            ret= client1.publish("aqua/lights", "off")
            ret= client1.publish("aqua/ato", "off")
            relayTest()

    else:
        relayTest()

def dosingTest():
    clear = os.system('clear')
    print("")
    print("########################################\n")
    print("Dosing Pump Test")
    print("")
    print("[b] to go back | [q] quit | [o] TURN OFF PSU\n")
    dose = input("Enter Dose Ammount(ml): ")
    if (dose.isnumeric()):
        ret= client1.publish("aqua/dosing", int(dose))
    elif dose == 'b':
        menu()

    elif dose == 'q':
        exit()

    elif dose == 'o':
        myPSU.setOutputState(0)
        myPSU.setOutputState(0)

    dosingTest()

def relayControl():
    clear = os.system('clear')
    print("\n")
    print("RELAY CONTROL")
    print("     [1] RELAY 1")
    print("     [2] RELAY 2")
    print("     [b] Return to Main Menu | [q] Quit")
    print()
    selection = input("Enter Selection: ")

    if selection == '1':
        def relay1Control():
            print("\n")
            print("     [1] Relay 1 ON")
            print("     [2] Relay 1 OFF")
            print("     [b] Back | [q] Quit")
            print("")

            toggle = input("Enter Selection: ")

            if toggle == '1':
                ret= client1.publish("aqua/lights", 'on')
                relay1Control()

            elif toggle == '2':
                ret= client1.publish("aqua/lights", 'off')
                relay1Control()

            elif toggle == 'b':
                relayControl()

            elif toggle == 'q':
                exit()

            else:
                menu()
        relay1Control()

    elif selection == '2':

        def relay2Control():
            print("\n")
            print("     [1] Relay 2 ON")
            print("     [2] Relay 2 OFF")
            print("     [b] Back | [q] Quit")
            print("")

            toggle2 = input("Enter Selection: ")

            if toggle2 == '1':
                ret= client1.publish("aqua/ato", 'on')
                relay2Control()
                

            elif toggle2 == '2':
                ret= client1.publish("aqua/ato", 'off')
                relay2Control()


            elif toggle2 == 'b':
                relayControl()

            elif selection == 'q':
                exit()

            else:
                menu()
        
        relay2Control()

    elif selection == 'b':
        menu()

    elif selection == 'q':
        exit()

    else:
        relayControl()

def psuSet():
    clear = os.system('clear')
    print("PSU Parameter Control\n")
    print("Turning Output Off")
    curStats = myPSU.getStats()
    currentSetVoltage = curStats[0] / 100
    currentSetCurrent = curStats[1] / 1000
    print("Curretly Set Parameters | V: %svdc A: %sA" % (currentSetVoltage, currentSetCurrent))
    inputV = input("Enter PSU Voltage Setpoint: ")
    inputA = input("Enter PSU Current Setpoint: ")
    print("Set V to %sVDC and set A to %sA ??" % (inputV, inputA))
    print("     [1] Confirm")
    print("     PRESS ANY KEY TO ABORT\n")
    confirm = input("Confirm?: ")
    if confirm == '1':
        try:
            myPSU.setVandC(float(inputV), float(inputA))
            curStats = myPSU.getStats()
            currentSetVoltage = curStats[0] / 100
            currentSetCurrent = curStats[1] / 1000
            print("Curretly Set Parameters | V: %svdc A: %sA" % (currentSetVoltage, currentSetCurrent))
        except:
            print("## AN ERROR HAS OCCURED ##")
            menu()

    else:
        menu()
    

def statStream():
    try:
        while (True):
            clear = os.system('clear')
            try:
                myPSU.printStats()
            except:
                pass
            time.sleep(0.25)
    except KeyboardInterrupt:
        menu()

def flashReset():
    status = myPSU.getStats()
    clear = os.system('clear')
    print("")
    print("########################################\n")
    print("Flash Reset")
    print("")
    print("Press 1 when flashing is compleate and flash cable is disconnected")
    print("[b] to go back | [q] quit\n")

    confirm = input("Ready for reset?: ")
    if confirm == '1':
        if status[5] == 1:
            print("Resetting ESP32 NOW")
            myPSU.setOutputState(0)
            time.sleep(2)
            myPSU.setOutputState(1)
        else:
            print("PSU IS NOT ON!!!")
        menu()
    
    elif confirm == 'b':
        menu()

    elif confirm == 'q':
        exit
    
    else:
        flashReset()



def menu():
    clear = os.system("clear")
    print("\n")
    print("########################################")
    print("")
    print("     Aquarium Controller Test Bench")
    print("")
    myPSU.printStats()
    print("")
    print("     [1] Load Power Supply Parameters")
    print("     [2] Turn ON Powersupply")
    print("     [3] RELAY TEST")
    print("     [4] DOSING TEST")
    print("     [5] Relay Control")
    print("     [6] PSU Parameter Control")
    print("     [7] PSU Stat Stream")
    print("     [o] TURN OFF POWERSUPPLY")
    print("     [r] Flash Reset")
    print("     [x] Shutdown and Quit")
    print("     [q] Quit")
    print("")
    print("########################################")
    print("")
    answer = input("Enter Selection: ")

    if answer == '1':
        myPSU.setVandC(12.00, 0.350)
        myPSU.printStats()
        menu()

    elif answer == '2':
        myPSU.setOutputState(1)
        myPSU.printStats()
        menu()

    elif answer == '3':
        relayTest()

    elif answer == '4':
        dosingTest()

    elif answer == '5':
        relayControl()

    elif answer == '6':
        psuSet()

    elif answer == '7':
        statStream()

    elif answer == 'o':
        myPSU.setOutputState(0)
        myPSU.setOutputState(0)
        myPSU.printStats()
        menu()

    elif answer == 'r':
        flashReset()
    elif answer == 'x':
        myPSU.setOutputState(0)
        exit()

    elif answer == 'q':
        exit()

    else:
        menu()

menu()
