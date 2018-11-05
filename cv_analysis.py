## FileName : cv_analysis.py
## Author: Joana Pasquali
## Calculate peak current from cyclic voltametry data
## Detect and remove value of capacitive current (background) from cyclic voltametry data 
## Created on november 5th 2018

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt


## Provide list of the names of the files to be processed  
fileNames = ['PadraoK3_Gaiola_cell3eletrodos.txt'] 

## Import file to pandas dataFrame
for filename in fileNames:
	data = pd.read_csv(filename, sep='\t',decimal=",")
	print(data.head()) 

## Differenciante data 
dy = np.diff(pd.to_numeric(data['I /uA.1']))

print(dy[1:20])

## Calculate moving average for 20 and 50 points --------
ma20 = []
ma50 = []

for i in range(len(dy)-20): 
	soma = 0 
	for k in range(0,20):
		soma = soma + dy[i+k]
	ma20.append(soma/20)
	
for i in range(len(dy)-50): 
	soma = 0 
	for k in range(0,50):
		soma = soma + dy[i+k]
	ma50.append(soma/50)
	
print(ma20[1:20])
print(ma50[1:20])

##--------------------------
