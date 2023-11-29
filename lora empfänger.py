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

def wait_2_send():
    trigger=b'<'
    output=1
    while output!=trigger:
        output= ser.read(size=1)
        print("wait_2 send - while")
        

ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

time.sleep(0.1)
input_1=ser.write(b'reboot\n')
print("sleep start")
time.sleep(1)
print("sleep end")
#ser.write(b'sx1280 rx start')
time.sleep(0.5)
ser.write(b'sx1280 rx start\n')
time.sleep(0.5)
while True:
    print("while oben")
    #output= ser.read(size=10)
    #output= ser.read_until(expected=b']',size=18)
    output= ser.readline()
    print(output)


ser.close()