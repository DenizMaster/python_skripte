#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 12:59:14 2023

@author: lora
"""

import fabric
import serial
import os
HOSTS=['10.42.0.1','10.42.0.2']

test_cmd = "ping " + HOSTS[0]


c1=fabric.Connection(HOSTS[0])
c1.run("cd ~/pythonscript/python_skripte")
c1.run("python3 'lora\ empfänger.py'")
#output=c1.run("ip addr\n")
#print(output)