#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 11:54:51 2023

@author: lora
"""
import serial
import time
#import threading

        
ser = serial.Serial('/dev/ttyACM0', baudrate=115200)

time.sleep(0.1)
input_1=ser.write(b'reboot\n')
print("sleep start")
time.sleep(1)
print("sleep end")
#ser.write(b'sx1280 rx start')
time.sleep(0.5)

for i in range(100):
    i_str=str(i)
    i_byte=i_str.encode()
    print("test")
    print(b'test '+i_byte)
    print(b'bla '+str(i).encode())
    ausgabe=ser.write(b'sx1280 tx '+str(i).encode()+b'\n')
    print(ausgabe)
    #ser.write(b'sx1280 tx hallo')
    time.sleep(0.5)

#outpurt=ser.write(b'sx1280 tx hallo')
#print(outpurt)
time.sleep(5)
ser.close()