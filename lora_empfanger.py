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
import os

ser = serial.Serial('/dev/ttyACM0', baudrate=115200)


time_now_dateiname_str=time.strftime("%d-%m-%Y_%X")
counter=0
kopf_der_spalten=["Index","RSSI","SNR"]
#dateiname = '~/Dokumente/CSV_datei/testdaten '+time_now_dateiname_str+'.csv'
dateiname = 'testdaten_'+time_now_dateiname_str+'.csv'

os.system("> "+dateiname)
datenbank = open(dateiname,mode='w',newline='\n')
csv.writer(datenbank).writerow(kopf_der_spalten)

time.sleep(0.1)
input_1=ser.write(b'reboot\n')
print("sleep start")
time.sleep(1)
print("sleep end")
time.sleep(0.5)
ser.write(b'sx1280 rx start\n')
time.sleep(0.5)
while counter<100:
    print("while oben")
    #output= ser.read(size=10)
    #output= ser.read_until(expected=b']',size=18)
    time_now_timestamp=time.strftime("%X_%x")#dt.datetime.now()
    output= str(ser.readline())
    output=output.replace("b","")
    output=output.replace("'","")
    #print(output[0])
    
    #output=output.replace(output[0],int(output[0]))
    output=output.replace("Data reception started\\n","")
    output=output.split("X")
    output[0]=ord(output[0])
    output.append(time_now_timestamp)
    #csv.writer(datenbank).writerow(output_list)
    print(output)
    #print(type(output))
    
    if counter==100:
        print("if in while")
        counter=0
    
    counter=counter+1
    
    


ser.close()