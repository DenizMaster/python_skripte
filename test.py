#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:01:04 2023

@author: lora
"""

#import os
import serial
import time
#import threading
def wait_2_send():
    trigger=b'<'
    output=1
    while output!=trigger:
        output= ser.read(size=1)
        print("wait_2 send - while")
        

ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

#stream = os.popen('BOARD=nucleo-l073rz make -C ~/RIOT/tests/driver_sx1280 term')
#output= stream.read()
#print(output)

input_1=ser.write(b'reboot')
#wait_2_send()
print("sleep start")

time.sleep(1)
print("sleep end")
ser.write(b'sx1280 rx start')
time.sleep(0.5)
while True:
    #print("while oben")
    #output= ser.read(size=1)
    #output= ser.read_until(expected=b']',size=18)
    output= ser.readlines()
    print(output)
    print("lauft")

ser.close()