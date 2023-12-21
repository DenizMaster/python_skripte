#tests zur vorbereitung der abspeicherung der daten in csv dateien

#import csv
#from datetime import date
import time
import pandas as pd

path_to_csv_file="C:/Users/deniz/Masterthesis_git/python_skripte/python_skripte/csv"
file_name="/datei"
file_end=".csv"
hallo="hallo"
saved_data="/Dataset_test.csv"
#time_now=date.ctime()

gesammtname=path_to_csv_file+file_name+time.strftime("%d.%m.%Y_%X")+file_end
print(gesammtname)

data_csv=pd.read_csv(path_to_csv_file+saved_data,sep=';',decimal=',')
data_csv=data_csv.drop(data_csv.index[0:44])
data_csv=data_csv.drop(['Unnamed: 2'],axis=1)
data_csv=data_csv.drop(['Unnamed: 3'],axis=1)
data_csv=data_csv.drop(['Unnamed: 4'],axis=1)

data_csv.head()


