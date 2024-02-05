#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Tue Nov 28 12:59:14 2023

@author: lora
'''

import fabric
import serial
import time
import os
import re

TTY='/dev/ttyACM0'

#TTY='/tmp/test'

HOSTS=['10.42.0.1','10.42.0.78']
c1=fabric.Connection(HOSTS[0])
c2=fabric.Connection(HOSTS[0])

#   einstellungen !!!

#######################################################################
payload_len='128'
sample_anz='61'
SF=['5']#,'6','7','8','9','10','11','12']
BW=['200']#,'400','800','1600']
CR=['1']#,'2']#,'3','4','5','6','7']
FREQ=['2479200000']#,'2400800000']
PWR=['-18']#,'-17','-16','-15','-14','-13','-12','-11','-10','-9','-8','-7','-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7','8','9','10','11','12','13']
Notiz='bild5:daempfung:80db' #keine unterstiche nutzen!!
##########################################################################


ser = serial.Serial(TTY, baudrate=115200)
cp=[(sf, bw, cr, freq,pwr) for sf in SF for bw in BW for cr in CR for freq in FREQ for pwr in PWR]

c1.put('/home/lora/Dokumente/lora_empfanger.py', '/home/lora/pythonscript/python_skripte/lora_empfanger.py')

for (sf, bw, cr, freq, pwr) in cp:

   
    c1.run('rm -f /home/lora/Documents/CSV_datei/endesingnal.txt')
    c1.run('rm -f /home/lora/Documents/CSV_datei/testdatei.dat')
    empfangerstart_str='screen python3 /home/lora/pythonscript/python_skripte/lora_empfanger.py 5 200 1 2479200000 >& /dev/null < /dev/null&'
    #empfangerstart_str='nohup python3 /home/lora/pythonscript/python_skripte/lora_empfanger.py '+sf+' '+bw+' '+cr+' '+freq+' &> /dev/null &'
    #print('drach -n `mktemp -u /tmp/%s.XXXX` %s' % ("dtach",empfangerstart_str))
    #c1.run(empfangerstart_str)
    time.sleep(0.1)
    input_1=ser.write(b'reboot\n')
    #print('zeile 50')
    time.sleep(2)
    ser.write(b'sx1280 set sf '+sf.encode()+b'\n')
    time.sleep(0.1)
    ser.write(b'sx1280 set bw '+bw.encode()+b'\n')
    time.sleep(0.1)
    ser.write(b'sx1280 set cr '+cr.encode()+b'\n')
    time.sleep(0.1)
    ser.write(b'sx1280 set freq '+freq.encode()+b'\n')
    time.sleep(0.1)
    ser.write(b'sx1280 set pwr '+pwr.encode()+b'\n')
    time.sleep(0.1)
    #print('zeile 62 2,5 sek später')
    
    ausgabe=ser.write(b'sx1280 tx_flooding '+sample_anz.encode()+b' '+payload_len.encode()+b'\n')
    
    while True:
        usgabe=ser.readline()
        output=usgabe.decode('ASCII').rstrip()
        #re.search(r'the End',output)
        print(output)
        #print('hallo')
        if re.search(r'the End',output):
            time_now_dateiname_str=time.strftime('%d-%m-%Y-%X')
            print('ende erreicht')
            c1.run('touch /home/lora/Documents/CSV_datei/endesingnal.txt')
            time.sleep(1)
            c1.get('/home/lora/pythonscript/python_skripte/testdaten.dat','/home/lora/Dokumente/CSV_datei/testdaten_'+time_now_dateiname_str+'_SF_'+sf+'_BW_'+bw+'_CR_'+cr+'_FREQ_'+freq+'_PWR_'+pwr+'_samples_'+sample_anz+'_'+Notiz+'_.dat')
            time.sleep(1.5)
             
            break

    
ser.close()
