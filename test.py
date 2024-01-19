"""
ruft über ssh auf dem zielrechner "test2.py" auf
um zu testen ob man per ssh den befehl zum start einer pythondatei geben kann 
"""
import fabric
import serial
import time
import os
from threading import Thread



HOSTS=['10.42.0.1','10.42.0.78']
c1=fabric.Connection(HOSTS[0])


#def ssh_verbindung():
      
c1.run("python3 ~/pythonscript/python_skripte/test2.py")
    #messdaten_liste=[]
    #while True:
     #   recl=c1.run("ls ~/pythonscript/python_skripte")
      #  daten=str(recl).split("\n")


CR=[1,2,3,4]
bw=[5,6,7,8,9]


for i in CR:
    for j in bw:
        print (i+j)

cp = [(sf, bw, cr) for sf in SF for bw in BW for cr in CR]
[(0,0,1),
 (0,0,2)]

for (sf, bw, cf) in cp:
    print(sf)
    print(bw)

for tpl in cp:
    sf = tpl[0]
    print(sf)
    print(bw)