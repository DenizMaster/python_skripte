import fabric
import serial
import time
import os


power_liste=[b'-18',b'-17',b'-16',b'-15',b'-14',b'-13',b'-12',b'-11',b'-10',b'-9',b'-8',b'-7',b'-6',b'-5',b'-4',b'-3',b'-2',b'-1',b'0',b'1',b'2',b'3',b'4',b'5',b'6',b'7',b'8',b'9',b'10',b'11',b'12',b'13']
ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
time.sleep(0.1)
input_1=ser.write(b'reboot\n')

time.sleep(1)
ausgabe=ser.write(b'sx1280 set freq 2.499.200.000\n')
print(ausgabe)
asfd=input("weiter?")
time.sleep(0.1)
ausgabe=ser.write(b'sx1280 tx_constwave\n')
time.sleep(0.1)
for i in power_liste:
    usgabe=ser.write(b'sx1280 set '+i)
    print(usgabe)
    asfd=input("weiter?")

   
#print(ausgabe)
time.sleep(5)
#ser.close()d
