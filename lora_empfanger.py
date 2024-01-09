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
dateiname = "testdaten_"+time_now_dateiname_str+".csv"
dateiname_beenden = '~/pythonscript/python_skripte/ende.txt'
dateiname2 = "testdaten_test.csv"
try:
    os.system("rm "+dateiname_beenden)
finally:
    print("gibts noch nciht")
#os.system("> "+dateiname2)
time.sleep(1)
open(dateiname,mode='x',newline='\n')
datenbank = open(dateiname,mode='a',newline='\n')
csv.writer(datenbank).writerow(kopf_der_spalten)

time.sleep(0.1)
input_1=ser.write(b'reboot\n')
print("sleep start")
time.sleep(1)
print("sleep end")
time.sleep(0.5)
ser.write(b'sx1280 rx start\n')
time.sleep(0.5)
output=0
while 1:#counter<100:
    print("while oben")
    #output= ser.read(size=10)
    #output= ser.read_until(expected=b']',size=18)
    #time_now_timestamp=time.strftime("%X_%x")#dt.datetime.now()
    output= str(ser.readline())
    
    output=output.replace("Data","")
    output=output.split(" ")
    try:
        del output[2]
        del output[3]
        del output[4]
        del output[5]
        del output[5]
    except IndexError:
        print("ignoring the first run")
    #output=output.replace("X","")
    #output=output.replace("'","")
    #print(output[0])
    
    #output=output.replace(output[0],int(output[0]))
    #output=output.replace("Data reception started\\n","")
    
    #output=output[0:1,3,5,7]
    #print(output[0])
    
    #output.append(time_now_timestamp)
    csv.writer(datenbank).writerow(output)
    print(output)
    #print(type(output))
    
    if output[1]==output_old[1]:
        break
    output_old=output
os.system("> "+dateiname_beenden)
    
    


ser.close()