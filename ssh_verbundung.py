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

TTY="/dev/ttyACM0"

#TTY="/tmp/test"

HOSTS=['10.42.0.1','10.42.0.78']
c1=fabric.Connection(HOSTS[0])
c2=fabric.Connection(HOSTS[0])

payload_len="128"
SF=["5","6","7","8","9","10","11","12"]
BW=["200","400","800","1600"]
CR=["1","2","3","4","5","6","7"]
FREQ=["2498400000"]
ser = serial.Serial(TTY, baudrate=115200)
cp=[(sf, bw, cr, freq) for sf in SF for bw in BW for cr in CR for freq in FREQ]
for (sf, bw, cr, freq) in cp:

    c1.put("/home/lora/Dokumente/lora_empfanger.py", "/home/lora/pythonscript/python_skripte/lora_empfanger.py")

    c1.run('rm -f /home/lora/Documents/CSV_datei/endesingnal.txt')
    c1.run("nohup python3 -u /home/lora/pythonscript/python_skripte/lora_empfanger.py "+sf+" "+bw+" "+cr+" "+freq+">& /dev/null < /dev/null&")

    time.sleep(0.1)
    input_1=ser.write(b'reboot\n')
    time.sleep(5)
    ser.write(b'sx1280 set sf '+sf+b'\n')
    time.sleep(0.5)
    ser.write(b'sx1280 set bw '+bw+b'\n')
    time.sleep(0.5)
    ser.write(b'sx1280 set cr '+cr+b'\n')
    time.sleep(0.5)
    ser.write(b'sx1280 set freq '+freq+b'\n')
    time.sleep(0.5)

    
    ausgabe=ser.write(b'sx1280 tx_flooding 1000 '+payload_len.encode()+b'\n')
    
    while True:
        usgabe=ser.readline()
        output=usgabe.decode("ASCII").rstrip()
        #re.search(r"the End",output)
        print(output)
        #print("hallo")
        if re.search(r"the End",output):
            time_now_dateiname_str=time.strftime("%d-%m-%Y_%X")
            print("ende erreicht")
            c1.run("touch /home/lora/Documents/CSV_datei/endesingnal.txt")
            time.sleep(2)
            c1.get("/home/lora/Documents/CSV_datei/testdaten.dat","/home/lora/Dokumente/CSV_datei/testdaten_"+time_now_dateiname_str+"_SF-"+sf+"_BW-"+bw+"_CR-"+cr+"_FREQ-"+freq+".dat") 
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