#tests zur vorbereitung der abspeicherung der daten in csv dateien


#from datetime import date
import time
#import numpy as np
#import pandas as pd
#import matplotlib as plt
import csv

path_to_csv_file="C:/Users/deniz/Masterthesis_git/python_skripte/python_skripte/csv"
file_name="/datei"
file_end=".csv"
hallo="hallo"
saved_data="/Dataset_test.csv"
#time_now=date.ctime()

gesammtname=path_to_csv_file+file_name+time.strftime("%d.%m.%Y_%X")+file_end
#gesammtname=[path_to_csv_file,file_name,time.strftime("%d.%m.%Y_%X"),file_end]


"""
data_csv=pd.read_csv(path_to_csv_file+saved_data,header=0,skiprows=43,usecols=[0,1],sep=';',decimal=',')
data_csv.head()
data_csv.plot(x="Frequency [Hz]",y="Magnitude [dBm]")
"""

file=open(path_to_csv_file+saved_data,mode='w',newline='')
gesammtname=gesammtname.split("/")
csv.writer(file).writerow(gesammtname)
print(gesammtname)
