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
#import datetime as dt
#import csv
import os
import argparse

parser = argparse.ArgumentParser()
                    #prog='ProgramName')#,
                    #description='What the program does',
                    #epilo='Text at the bottom of help')
parser.add_argument('SF')
parser.add_argument('BW')
parser.add_argument('CR')
parser.add_argument('FREQ')
args=parser.parse_args()
#print(args.SF)
ser = serial.Serial('/dev/ttyACM0', baudrate=115200,timeout=1)


time_now_dateiname_str=time.strftime("%d-%m-%Y_%X")
counter=0
kopf_der_spalten=["Index","RSSI","SNR"]

dateiname = "testdaten.dat"


time.sleep(0.1)


datenbank = open(dateiname,mode="w",newline="\n")
datenbank.write("hallo;hallo \n")

time.sleep(0.1)
input_1=ser.write(b'reboot\n')
print("sleep start")
time.sleep(0.1)
print("sleep end")
time.sleep(0.1)
datenbank.write("hallo;hallo \n")
ser.write(b'sx1280 set sf '+args.SF.encode()+b'\n')
time.sleep(0.1)
ser.write(b'sx1280 set bw '+args.BW.encode()+b'\n')
time.sleep(0.1)
ser.write(b'sx1280 set cr '+args.CR.encode()+b'\n')
time.sleep(0.1)
ser.write(b'sx1280 set freq '+args.FREQ.encode()+b'\n')
time.sleep(0.1)
ser.write(b'sx1280 rx start\n')
time.sleep(0.1)
datenbank.write("hallo;hallo \n")
while True:
    #print("while oben")
    if os.path.exists("/home/lora/Documents/CSV_datei/endesingnal.txt"):
        break

    time_now_timestamp=time.strftime("%X_%x")#dt.datetime.now()
    outputt=ser.readline().decode("ASCII").rstrip()
    #print("T", outputt)
    if outputt == "":
        continue
    #output= [outputt,time_now_timestamp]

    zeile=f"{time_now_timestamp};{outputt}"
    #csv.writer(datenbank).writerow(output)
    datenbank.write(zeile+"\n")
   

print("fertig")
datenbank.close()
ser.close()