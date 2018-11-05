## FileName : cv_analysis.py
## Author: Joana Pasquali
## Calculate peak current from cyclic voltametry data
## Detect and remove value of capacitive current (background) from cyclic voltametry data 
## Created on november 5th 2018

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

#------------- funcs -----------------

    



#------------- main ------------------

# Provide list of the names of the files to be processed  
fileNames = ['PadraoK3_Gaiola_cell3eletrodos.txt'] 

# Import file to pandas dataFrame
for filename in fileNames:
	data = pd.read_csv(filename, sep='\t',decimal=",") # Importa o arquivo para um pandas dataframe
	print(data.head())
#data = pd.read_csv(item, sep='\t',decimal=",") 
 
#print(data.head())
