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
import re




HOSTS=['10.42.0.1','10.42.0.78']
c1=fabric.Connection(HOSTS[0])
c2=fabric.Connection(HOSTS[0])

spreading_faktors=["1","2","3","4"]
BW=["200","400","800"]

c1.run("python3 ~/pythonscript/python_skripte/lora_empfanger.py &")

print("geht weiter")
ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
time.sleep(0.1)
input_1=ser.write(b'reboot\n')

time.sleep(1)

ausgabe=ser.write(b'sx1280 tx_flooding 50\n')
print(ausgabe)
while True:
    usgabe=ser.readline()
    output=usgabe.decode("ASCII").rstrip()
    #re.search(r"the End",output)
    print(output)
    #print("hallo")
    if re.search(r"the End",output):
        time_now_dateiname_str=time.strftime("%d-%m-%Y_%X")
        print("ende erreicht")
        c1.get("~/Documents/CSV_datei/testdaten.csv","~/Dokumente/CSV_datei/testdaten_"+time_now_dateiname_str+".csv") #TODO: bei automatisierung auch unterschiedliche parameter einfügen
        break
#time.sleep(5)
    # regex
ser.close()

"""
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
    #os.system("scp lora@10.42.0.1:~/pythonscript/python_skripte/"+i+" lora@10.42.0.78 ~/Dokumente")
    c1.get()
"""