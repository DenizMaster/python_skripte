#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:59:14 2023

@author: lora
"""

import fabric 
import serial

import os
HOSTS=['10.42.0.1','10.42.0.78']

test_cmd = "ping " + HOSTS[1]


c1=fabric.Connection(HOSTS[0])
#for i in range(100):
#    recl=c1.run(test_cmd)
#    print(recl)
#    print(i)

#recl=c1.run("pwd")
#print(recl)
#recl=c1.run("> testdatei_12345.csv")
while 1:
    recl=c1.run("ls")
    #print(recl)
    daten=str(recl).split("\n")
    print(daten)
    messdaten_liste=[]
    for i in daten:
        if i.startswith("ende"):
            for j in daten:
                if j.startswith("testdaten"):
                    messdaten_liste.append(j)
            break

print(messdaten_liste)
#recl=c1.run("pwd")
#print(recl)
#c1.run("-C ~/Documents  > testdatei_123.csv")
for i in messdaten_liste:
    os.system("scp lora@10.42.0.1:~/"+i+" ~/Dokumente")
#c1.run("python3 'lora\ empfänger.py'")
#output=c1.run("ip addr\n")
#print(output)