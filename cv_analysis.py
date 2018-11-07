## FileName : cv_analysis.py
## Author: Joana Pasquali
## Calculate peak current from cyclic voltametry data
## Detect and remove value of capacitive current (background) from cyclic voltametry data 
## Date: november 5th 2018

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

def media(vetor):
        soma = 0
        for x in vetor:
            soma = soma + x
        return soma / len(vetor)   

def soma(vetor):
        soma = 0
        for x in vetor:
            soma = soma + x
        return soma

def multiplica(vetor_x, vetor_y):
        soma = 0
        for x,y in zip(vetor_x, vetor_y):
            soma = soma + x * y
        return soma

def find_coeffs(x, y):
  
        soma_x = soma(x)
        soma_x2 = multiplica(x,x) 
        soma_xy = multiplica(x,y) 
        media_x = media(x)
        media_y = media(y)
        
        m = (soma_xy - soma_x * media_y) / (soma_x2 - soma_x * media_x)
        
        media_x = media(x)
        media_y = media(y)
        
        b = media_y - m * media_x
        
        return m, b

def y_predict(m, b, x):
    
    new_y = []
    for i in x:
        y = m * i + b
        new_y.append(y)
        
    return new_y    

def find_slope_idx(x, y, dy):

	## Calculate moving average for 20 and 50 points
	ma20 = []
	ma50 = []

	for i in range(len(dy)-50): 
		soma = 0 
		for k in range(0,50):
			soma = soma + dy[i+k]
		ma20.append(round(soma/50, 3))
		
	for i in range(len(dy)-75): 
		soma = 0 
		for k in range(0,75):
			soma = soma + dy[i+k]
		ma50.append(round(soma/75, 3))

	## Find intercepts of different moving average curves
	ma20_num = np.array(ma20)
	ma50_num = np.array(ma50)
	idx = np.argwhere(np.diff(np.sign(ma50_num - ma20_num[:len(ma50)]))!= 0).reshape(-1)+0
	
	## Uncomment to see whats going on 
	'''plt.plot(x[idx], ma20_num[idx], 'ro') ## Plot intersections 
	plt.plot(x[0:len(ma50)], ma50, x[0:len(ma20)], ma20) ## Plot moving averages'''

	return int(idx[0])

def plot_lines(x, y, dy):

	idx = find_slope_idx(x, y, dy) + 25
	half_idx = int(0.5 * idx)
	m, b = find_coeffs(x[(idx - half_idx) : (idx + half_idx)], y[(idx - half_idx) : (idx + half_idx)])
	y_pred = y_predict(m, b, x)
	plt.plot(x, y_pred, color = "m")
	
	return y_pred
	
def main():

	## File names list needs to be provided
	fileNames = ['SPE_FC_3.txt','SPE_Gaiola_2.txt','PadraoK3_Gaiola_cell3eletrodos.txt']

	## Import file to pandas dataFrame
	for filename in fileNames:

		data = pd.read_csv(filename, sep='\t',decimal=",")

		## Differenciante data 
		x = pd.to_numeric(data['E /V'])
		y = pd.to_numeric(data['I /uA.1'])
		dy = np.diff(y)/(np.diff(x)) # 0.0035 
	
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
		plt.plot(x1, y1, x2, y2)
		plt.xlabel('Eixo X')
		plt.ylabel('Eixo Y')

		## Find linear regression and predicted line	
		y_pred1 = plot_lines(x1,y1, dy1)
		y_pred2 = plot_lines(x2,y2, dy2)
	
		## Finds min and max peaks
		min_pos = y1.argmin() 
		max_pos = y2.argmax()
	
		plt.plot( x1[min_pos], y1[min_pos], 'bo')
		plt.plot( x2[max_pos], y2[max_pos], 'bo')
	
		max_pot = x2[max_pos]
		max_cur = y2[max_pos] - y_pred1[max_pos]
		min_pot = x1[min_pos]
		min_cur = y1[min_pos] - y_pred2[min_pos]
	
		print max_cur, max_pot, min_cur, min_pot
	
		plt.savefig(filename + '_saida.png')
		plt.show()

if __name__ == "__main__":
    main()
		 
