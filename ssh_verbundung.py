#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:59:14 2023

@author: lora
"""

import fabric
import serial
import time
import os
from threading import Thread



HOSTS=['10.42.0.1','10.42.0.78']
c1=fabric.Connection(HOSTS[0])
c2=fabric.Connection(HOSTS[0])

def ssh_python_start():
    c2.run("python3 ~/pythonscript/python_skripte/lora_empfanger.py")
    

def ssh_verbindung():
      
    #c1.run("python3 ~/pythonscript/python_skripte/lora_empfanger.py")
    messdaten_liste=[]
    while True:
        recl=c1.run("ls ~/pythonscript/python_skripte")
        daten=str(recl).split("\n")
        for i in daten:
            if i.startswith("ende"):
                for j in daten:
                    if j.startswith("testdaten"):
                        messdaten_liste.append(j)
                break
            
    #print(messdaten_liste)
    for i in messdaten_liste:
        os.system("scp lora@10.42.0.1:~/pythonscript/python_skripte/"+i+" lora@10.42.0.78 ~/Dokumente")

#recl=c1.run("pwd")
#print(recl)
#c1.run("-C ~/Documents  > testdatei_123.csv")
#c1.run("python3 'lora\ empfänger.py'")
#output=c1.run("ip addr\n")
#print(output)
def lora_sender():
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
    time.sleep(0.1)
    input_1=ser.write(b'reboot\n')
    print("sleep start")
    time.sleep(1)
    print("sleep end")
    #ser.write(b'sx1280 rx start')
    time.sleep(0.5)
    ausgabe=ser.write(b'sx1280 tx_flooding 1000\n')
    print(ausgabe)
    time.sleep(5)
    ser.close()

ssh_thread=Thread(target=ssh_verbindung)
sending_thread=Thread(target=lora_sender)

ssh_thread.start()
sending_thread.start()