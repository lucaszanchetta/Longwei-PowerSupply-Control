import tkinter as tk
import tkinter.font as tkFont
from lwModbusTCP import PSU
import time

root = tk.Tk()

# Main Title Text
title = "Power Supply Control"
message = tk.Label(root, text=title, height=3, width=(len(title)+8))
messageFont = tkFont.Font(size=22)
message.configure(font=messageFont)
message.pack()

readoutFont = tkFont.Font(size=12)

# Connects to PSU
myPSU = PSU('192.168.1.200', False)

def setParams():
    vSet = ent_vSet.get()
    aSet = ent_aSet.get()
 
    myPSU.setVandC(float(vSet), float(aSet))

def psuToggleOutput():
    myPSU.getStats()
    
    if myPSU.state == "ON":
        myPSU.setOutputState(0)

    elif myPSU.state == "OFF":
        myPSU.setOutputState(1)

def stats():
    myPSU.getStats()
    frm_stats = tk.Frame(master=root, relief=tk.RIDGE, borderwidth=1)

    global lbl_oS, lbl_oM, lbl_a, lbl_v, lbl_vSet, lbl_aSet

    v = "{}V".format(myPSU.v)
    lbl_v = tk.Label(master=frm_stats, text=v, padx=3, pady=3, relief=tk.RIDGE, borderwidth=1, width=12)
    lbl_v.configure(font=readoutFont)
    lbl_v.grid(row=0, column=0)

    a = "{}A".format(myPSU.a)
    lbl_a = tk.Label(master=frm_stats, text=a, padx=3, pady=3, relief=tk.RIDGE, borderwidth=1, width=12)
    lbl_a.configure(font=readoutFont)
    lbl_a.grid(row=0, column=1)

    oM = "Mode: {}".format(myPSU.outputMode)
    lbl_oM = tk.Label(master=frm_stats, text=oM, padx=3, pady=3, relief=tk.RIDGE, borderwidth=1, width=12)
    lbl_oM.configure(font=readoutFont)
    lbl_oM.grid(row=0, column=2)


    vSet = "Set V: {}".format(myPSU.vSetPoint)
    lbl_vSet = tk.Label(master=frm_stats, text=vSet, padx=3, pady=3, relief=tk.RIDGE, borderwidth=1, width=12)
    lbl_vSet.configure(font=readoutFont)
    lbl_vSet.grid(row=1, column=0)

    aSet = "Set A: {}".format(myPSU.aSetPoint)
    lbl_aSet = tk.Label(master=frm_stats, text=aSet, padx=3, pady=3, relief=tk.RIDGE, borderwidth=1, width=12)
    lbl_aSet.configure(font=readoutFont)
    lbl_aSet.grid(row=1, column=1)

    oS = myPSU.getOutputState()
    oSText = "STATE: {}".format(oS)
    lbl_oS = tk.Label(master=frm_stats, text=oSText, padx=3, pady=3, relief=tk.RIDGE, borderwidth=1, width=12)
    lbl_oS.configure(font=readoutFont)
    lbl_oS.grid(row=1, column=2)

    frm_stats.pack()

def stateInvert():
        currState = myPSU.state

        if currState == "ON":
            return "OFF"

        elif currState == "OFF":
            return "ON"
        
        else:
            return "ERR"

def outputUpdate():


    global btn_output

    stateText = stateInvert()
    btn_output = tk.Button(master=paramButtons, text=stateText, command=psuToggleOutput, padx=5, pady=5)
    btn_output.grid(row=0, column=1, padx=10, pady=5)


def Refresher():
    global lbl_oS, lbl_oM, lbl_a, lbl_v, lbl_vSet, lbl_aSet, btn_output
    time.sleep(0.5)
    myPSU.getStats()

    oS = myPSU.getOutputState()
    oSText = "STATE: {}".format(oS)
    lbl_oS.configure(text=oSText)
    
    v = "{}V".format(myPSU.v)
    lbl_v.configure(text=v)

    a = "{}A".format(myPSU.a)
    lbl_a.configure(text=a)

    oM = "Mode: {}".format(myPSU.outputMode)
    lbl_oM.configure(text=oM)

    vSet = "Set V: {}".format(myPSU.vSetPoint)
    lbl_vSet.configure(text=vSet)

    aSet = "Set A: {}".format(myPSU.aSetPoint)
    lbl_aSet.configure(text=aSet)

    stateText = stateInvert()
    btn_output.configure(text=stateText)

    root.after(1000, Refresher)

stats()

paramControls = tk.Frame(master=root, padx=10, pady=10, relief=tk.RIDGE, borderwidth=1, width=150)
paramInput = tk.Frame(master=paramControls, padx=5, pady=5)
paramInput.grid(row=0, column=0)
paramButtons = tk.Frame(master=paramControls, padx=10, pady=10)
paramButtons.grid(row=1, column=0)

msg_vSet = tk.Message(master=paramInput, text="Voltage Setpoint")
msg_vSet.grid(row=0, column=0)
ent_vSet = tk.Entry(master=paramInput, width=15, font=("default", 12))
ent_vSet.grid(row=1, column=0)

msg_aSet = tk.Message(master=paramInput, text="Current Setpoint")
msg_aSet.grid(row=2, column=0)
ent_aSet = tk.Entry(master=paramInput, width=15, font=("default", 12))
ent_aSet.grid(row=3, column=0)

btn_set = tk.Button(master=paramButtons, text="SET", command=setParams, padx=5, pady=5)
btn_set.grid(row=0, column=0, padx=10, pady=5)

outputUpdate()

paramControls.pack()

Refresher()

# keep the window displaying
root.mainloop()