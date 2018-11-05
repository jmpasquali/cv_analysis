## FileName : cv_analysis.py
## Author: Joana Pasquali
## Calculate peak current from cyclic voltametry data
## Detect and remove value of capacitive current (background) from cyclic voltametry data 
## Date: november 5th 2018

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt


## ----------------------funcs ----------------------
def estimate_coef(x, y):
	# number of observations/points
	n = np.size(x)

	# mean of x and y vector
	m_x, m_y = np.mean(x), np.mean(y)

	# calculating cross-deviation and deviation about x
	SS_xy = np.sum(y*x - n*m_y*m_x)
	SS_xx = np.sum(x*x - n*m_x*m_x)

	# calculating regression coefficients
	b_1 = SS_xy / SS_xx
	b_0 = m_y - b_1*m_x

	return(b_0, b_1)

def plot_regression_line(x, y, b):
	# plotting the actual points as scatter plot
	#plt.scatter(x, y, color = "m", marker = "o", s = 30)

	# predicted response vector
	y_pred = b[0] + b[1]*x

	# plotting the regression line
	plt.plot(x, y_pred, color = "g")

	# putting labels
	plt.title('Calibracao Motor 1')

    
##-----------------------main-------------------------


## Provide list of the names of the files to be processed  
fileNames = ['PadraoK3_Gaiola_cell3eletrodos.txt'] 

## Import file to pandas dataFrame
for filename in fileNames:
	data = pd.read_csv(filename, sep='\t',decimal=",")
	print(data.head()) 

## Differenciante data 
x1 = pd.to_numeric(data['E /V'])
y1 = pd.to_numeric(data['I /uA.1'])
dy1 = np.diff(y1)/0.0035 #(np.diff(x1))

dy = dy1[1:500]
x = x1[1:500]
y = y1[1:500]
print(dy[1:20])

## Calculate moving average for 20 and 50 points --------
ma20 = []
ma50 = []

for i in range(len(dy)-20): 
	soma = 0 
	for k in range(0,20):
		soma = soma + dy[i+k]
	ma20.append(round(soma/20, 3))
	#ma20.append(soma/20)
for i in range(len(dy)-50): 
	soma = 0 
	for k in range(0,50):
		soma = soma + dy[i+k]
	ma50.append(round(soma/50, 3))
	#ma50.append(soma/50)
	
print(ma20[1:200])
print(ma50[1:200])
##--------------------------


plt.plot(x1, y1,x, dy, x[0:len(ma20)], ma20, x[0:len(ma50)], ma50)
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')


## Find intercepts of movingAverage curves
ma20_num = np.array(ma20)
ma50_num = np.array(ma50)
idx = np.argwhere(np.diff(np.sign(ma50_num - ma20_num[0:len(ma50)]))!= 0).reshape(-1)+0
print(idx)
plt.plot(x[idx], ma20_num[idx], 'ro')
critical_idx = idx[0]  #increment 0.1 because of delay

## Linear regression of data untill critical x
b = []
b = estimate_coef(x[0:idx[0]], y1[0:idx[0]])
print(b)
plot_regression_line(x, y, b)
plt.savefig('fig.png')
plt.show()
