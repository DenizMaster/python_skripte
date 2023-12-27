#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 12:38:01 2023

@author: lora

empfänger skript:
    empfängt nachrichten und speichert snr und rssi
    
    TODO: read command auspendeln
          daten abspeichern
"""



import serial
import time
import datetime as dt
import csv

ser = serial.Serial('/dev/ttyACM0', baudrate=115200)


time_now_dateiname_str=time.strftime("%d-%m-%Y_%X")
counter=0
kopf_der_spalten="kopf der spalten"#TODO muss noch angepasst werden
dateiname = '~/Dokumente/CSV_datei/messwerte '+time_now_dateiname_str+'.csv'
datenbank = open(dateiname,mode='w',newline='\n')
csv.writer(datenbank).writerow(kopf_der_spalten)

time.sleep(0.1)
input_1=ser.write(b'reboot\n')
print("sleep start")
time.sleep(1)
print("sleep end")
#ser.write(b'sx1280 rx start')
time.sleep(0.5)
ser.write(b'sx1280 rx start\n')
time.sleep(0.5)
while counter<10:
    print("while oben")
    #output= ser.read(size=10)
    #output= ser.read_until(expected=b']',size=18)
    time_now_timestamp=time.strftime("%X_%x")#dt.datetime.now()
    output= ser.readline()
    output=output.split("X")
    output_list=output.append(time_now_timestamp)
    csv.writer(datenbank).writerow(output_list)
    print(output)
    if counter==10:
        print("if in while")
        counter=0
    
    counter=counter+1
    
    


ser.close()