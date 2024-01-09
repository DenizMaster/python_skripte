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