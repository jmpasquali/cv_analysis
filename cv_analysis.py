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
from sklearn.linear_model import LinearRegression

## ----------------------funcs ----------------------
#--------------------------------------------------------
def media(vetor):
        soma = 0
        for x in vetor:
            soma = soma + x
        return soma / len(vetor)    

#--------------------------------------------------------
def soma(vetor):
        soma = 0
        for x in vetor:
            soma = soma + x
        return soma

#--------------------------------------------------------
def multiplica(vetor_x, vetor_y):
        soma = 0
        for x,y in zip(vetor_x, vetor_y):
            soma = soma + x * y
        return soma
        
#--------------------------------------------------------
def calcula_m(vetor_x, vetor_y):
    
        soma_x = soma(vetor_x)
        soma_x2 = multiplica(vetor_x,vetor_x) 
        soma_xy = multiplica(vetor_x,vetor_y) 
        media_x = media(vetor_x)
        media_y = media(vetor_y)
        
        m = (soma_xy - soma_x * media_y) / (soma_x2 - soma_x * media_x)
        
        return m
        
#--------------------------------------------------------
def calcula_b(m, vetor_x, vetor_y):
        
        media_x = media(vetor_x)
        media_y = media(vetor_y)
        
        b = media_y - m * media_x
        
        return b

#--------------------------------------------------------
def calcula_y_ajuste(m, b, vetor_x):
    
    ajuste_y = []
    for x in vetor_x:
        y = m * x + b
        ajuste_y.append(y)
        
    return ajuste_y    
            
           
#--------------------------------------------------------
def cria_grafico(vetor_x, vetor_y, ajuste_y, nome_grafico):
    
    plt.plot(vetor_x,vetor_y,'ro', vetor_x, ajuste_y,'b')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    
    plt.savefig(nome_grafico)
    plt.show();
    

def find_slope_idx(x, y, dy):

	## Calculate moving average for 20 and 50 points
	ma20 = []
	ma50 = []

	for i in range(len(dy)-20): 
		soma = 0 
		for k in range(0,20):
			soma = soma + dy[i+k]
		ma20.append(round(soma/20, 3))
		
	for i in range(len(dy)-75): 
		soma = 0 
		for k in range(0,75):
			soma = soma + dy[i+k]
		ma50.append(round(soma/75, 3))
		
	## Plot moving averages
	plt.plot(x[0:len(ma50)], ma50, x[0:len(ma20)], ma20)
		
	## Find intercepts of movingAverage curves
	ma20_num = np.array(ma20)
	ma50_num = np.array(ma50)
	idx = np.argwhere(np.diff(np.sign(ma50_num - ma20_num[:len(ma50)]))!= 0).reshape(-1)+0
	
	## Plot intersections 
	plt.plot(x[idx], ma20_num[idx], 'ro')
	
	return int(idx[0])

##-----------------------main-------------------------

## Provide list of the names of the files to be processed  
fileNames = ['PadraoK3_Gaiola_cell3eletrodos.txt','SPE_FC_3.txt','SPE_Gaiola_2.txt']
 
##SPE_FC_3.txt','SPE_Gaiola_2.txt'

## Import file to pandas dataFrame
for filename in fileNames:

	data = pd.read_csv(filename, sep='\t',decimal=",")
	print(data.head()) 

	## Differenciante data 
	x = pd.to_numeric(data['E /V'])
	y = pd.to_numeric(data['I /uA.1'])
	dy = np.diff(y)/0.0035 #(np.diff(x1))
	
	## Split Vectors (still needs some work)
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
	
	## Plot all data 
	plt.plot(x1, y1, x2, y2)#, x1, dy1, x2, dy2)
	plt.xlabel('Eixo X')
	plt.ylabel('Eixo Y')


	## Plot linear regression of first cycle
	idx1 = find_slope_idx(x1, y1, dy1)
	half_idx1 = int(0.5*idx1)
	m1 = calcula_m(x1[(idx1 - half_idx1) : (idx1 + half_idx1)], y1[(idx1 - half_idx1) : (idx1 + half_idx1)])
	b1 = calcula_b(m1, x1[(idx1 - half_idx1) : (idx1 + half_idx1)], y1[(idx1 - half_idx1) : (idx1 + half_idx1)])
	y_pred1 = calcula_y_ajuste(m1, b1, x1)
	plt.plot(x1, y_pred1, color = "m")
	
	#b1 = estimate_coef(np.array(x1[0:idx1[0]]), np.array(y1[0:idx1[0]]))
#	plot_regression_line(x1, y1, b1)
	

	## Not quite working yet 
	idx2 = find_slope_idx(x2, y2, dy2)
	half_idx2 = int(0.5*idx2)
	m2 = calcula_m(x2[(idx2 - half_idx2) : (idx2 + half_idx2)], y2[(idx2 - half_idx2) : (idx2 + half_idx2)])
	b2 = calcula_b(m2, x2[(idx2 - half_idx2) : (idx2 + half_idx2)], y2[(idx2 - half_idx2) : (idx2 + half_idx2)])
	
	y_pred2 = calcula_y_ajuste(m2, b2, x2)
	plt.plot(x2, y_pred2, color = "m")
	
	print x1, y1, x2, y2, y_pred2
	print idx2
	
	min_pos = y1.argmin() 
	max_pos = y2.argmax()
	
	print(min_pos, max_pos)
	plt.plot( x1[min_pos], y1[min_pos], 'bo')
	plt.plot( x2[max_pos], y2[max_pos], 'bo')
	
	plt.savefig(filename + '_saida.png')
	plt.show()
		
		
		 
