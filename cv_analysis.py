## FileName : cv_analysis.py
## Author: Joana Pasquali
## Calculate peak current from cyclic voltametry data
## Detect and remove value of capacitive current (background) from cyclic voltametry data 
## Date: november 5th 2018

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import copy 

## ----------------------funcs ----------------------
def estimate_coef(x, y):

	## Number of observations/points
	n = np.size(x)

	## Mean of x and y vector
	m_x, m_y = np.mean(x), np.mean(y)

	## Calculating cross-deviation and deviation about x
	SS_xy = np.sum(y*x - n*m_y*m_x)
	SS_xx = np.sum(x*x - n*m_x*m_x)

	## Calculate regression coefficients
	b_1 = SS_xy / SS_xx
	b_0 = m_y - b_1*m_x

	return(b_0, b_1)

def plot_regression_line(x, b):

	# predicted response vector
	y_pred = b[0] + b[1]*x

	# plotting the regression line
	plt.plot(x, y_pred, color = "m")

def find_slope_idx(x, y, dy):

	## Calculate moving average for 20 and 50 points
	ma20 = []
	ma50 = []

	for i in range(len(dy)-20): 
		soma = 0 
		for k in range(0,20):
			soma = soma + dy[i+k]
		ma20.append(round(soma/20, 3))
		
	for i in range(len(dy)-50): 
		soma = 0 
		for k in range(0,50):
			soma = soma + dy[i+k]
		ma50.append(round(soma/50, 3))
		
	plt.plot(x[0:len(ma50)], ma50, x[0:len(ma20)], ma20)#, y1, x2, y2, x1, dy1, x2, dy2)#, x[0:len(ma50)], ma50)
	## Find intercepts of movingAverage curves

	ma20_num = np.array(ma20)
	ma50_num = np.array(ma50)
	idx = np.argwhere(np.diff(np.sign(ma50_num - ma20_num[:len(ma50)]))!= 0).reshape(-1)+0
	print('idx ', idx)
	plt.plot(x[idx], ma20_num[idx], 'ro')
 
	## Linear regression of data untill critical x
	b = estimate_coef(np.array(x[0:idx[0]]), np.array(y[0:idx[0]]))
	print('coefs ', b)
	plot_regression_line(x, b)
	
	return idx
##-----------------------main-------------------------

## Provide list of the names of the files to be processed  
fileNames = ['PadraoK3_Gaiola_cell3eletrodos.txt'] #,'SPE_FC_3.txt','SPE_Gaiola_2.txt']
 
##SPE_FC_3.txt','SPE_Gaiola_2.txt'

## Import file to pandas dataFrame
for filename in fileNames:

	data = pd.read_csv(filename, sep='\t',decimal=",")
	print(data.head()) 

	## Differenciante data 
	x = pd.to_numeric(data['E /V'])
	y = pd.to_numeric(data['I /uA.1'])
	dy = np.diff(y)/0.0035 #(np.diff(x1))
	
	x_copy = np.array(x)
	y_copy = np.array(y)
	dy_copy = np.array(dy)
	
	half = int(len(dy)/2)
	end = int(len(dy))
	dy1 = dy_copy[0:half]
	x1 = x_copy[0:half]
	y1 = y_copy[0:half]
	
	dy2 = dy_copy[(half+1):end]
	x2= x_copy[(half+1):end]
	y2 = y_copy[(half+1):end]

	plt.plot(x1, y1, x2, y2, x1, dy1, x2, dy2)#, x[0:len(ma50)], ma50)
	plt.xlabel('Eixo X')
	plt.ylabel('Eixo Y')
	find_slope_idx(x1, y1, dy1)
	#find_slope_idx(x2, y2, dy2)
	
	idx = 	find_slope_idx(x2, y2, dy2)
	print(idx)
	## Linear regression of data untill critical x
	b = estimate_coef(x[510:524], y[510:524])
	print('coefs ', b)
	plot_regression_line(x2, b)
	
	
	print(x1)
	print(x2)
	plt.savefig(filename + '_saida.png')
	plt.show()
