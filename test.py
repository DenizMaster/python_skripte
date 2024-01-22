"""
ruft über ssh auf dem zielrechner "test2.py" auf
um zu testen ob man per ssh den befehl zum start einer pythondatei geben kann 
"""
import fabric
import serial
import time
import os
from threading import Thread



#HOSTS=['10.42.0.1','10.42.0.78']
#c1=fabric.Connection(HOSTS[0])


#def ssh_verbindung():
      
#c1.run("python3 ~/pythonscript/python_skripte/test2.py")
    #messdaten_liste=[]
    #while True:
     #   recl=c1.run("ls ~/pythonscript/python_skripte")
      #  daten=str(recl).split("\n")


CR=[1,2,3,4]
BW=["A","B","C"]
SF=["a","b","c"]


#for i in CR:
    #for j in bw:
        #print (i+j)

#cp = [(sf, bw, cr) for sf in SF for bw in BW for cr in CR]
#[(0,0,1),
# (0,0,2)]

#for (sf, bw, cr) in cp:
 #   print(sf)
  #  print(bw)
  #  print(cr)
   # print("punkt")
#a=b'hallo'
b=" test"
#b1=b.encode()
print(b'hallo'+b.encode())
for c in BW:
    print(c.encode())
#for tpl in cp:
 #   sf = tpl[0]
 #   print(sf)
 #  print(bw)