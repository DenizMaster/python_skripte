#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 13:22:19 2023

@author: lora
"""

import fabric
import serial
import os


start_cmd ="BOARD=nucleo-l073rz make -C RIOT/tests/drivers/sx1280 all flash term"
HOSTS =['lora@192.168.1.147','lora@192.168.1.222']



def linux_pc_receiver(self, test):
    test_cmd = "ping " + HOSTS[0]
    os.system(test_cmd)
    os.system(start_cmd)

def pi_transmitter(self, test):
    ser= serial.Serial('/dev/ttyACM0')

    c1=fabric.Connection(HOSTS[0])
    c2=fabric.Connection(HOSTS[1])

    c1.run("~")
    c1.run("cd /RIOT/tests/drivers/sx1280")
    #c1.run("export BUID_IN_DOCKER=1")
    c1.run("export BOARD=nucleo-l07rz")
    c2.run("make all flash term")
    c2.run("sx1280 rx start")
