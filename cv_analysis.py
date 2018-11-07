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
	plt.plot(x, y_pred, color = "fuchsia",linestyle=':',linewidth=2) #orangered ##
	
	return y_pred
	
	
def main():
	
	input =  raw_input('Name of csv containing file names list: ')
	
	## List of the names of the files needs to be provided
	fileNames = [input]#,'SPE_Gaiola_2.txt','PadraoK3_Gaiola_cell3eletrodos.txt']

	# Import the files names from the file Nomes.csv
	inputList = []
	with open(input,'rb') as csvfile:
	    spamreader = csv.reader(csvfile, delimiter=',', quotechar = '|')
	    for row in spamreader:
		name = str(row[0])
		inputList.append(name)
             
	## Import file to pandas dataFrame
	out_data ={}
	for filename in inputList:

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
		plt.plot(x1, y1,'dodgerblue',linewidth=1) ##darkgrey
		plt.plot(x2, y2,'dodgerblue', linewidth=1) ##dodgerblue
		plt.xlabel(' E [V]' )
		plt.ylabel(' I [uA] ')
		plt.title(filename)
		plt.grid(color='0', linewidth=0.1)
		ax = plt.subplot(111)    
		ax.spines["top"].set_visible(False)    
	#	ax.spines["bottom"].set_visible(False)    
		ax.spines["right"].set_visible(False)    
	#	ax.spines["left"].set_visible(False) 
	#	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")   
		plt.xticks(fontsize=8)  
		plt.yticks(fontsize=8)  

		
		## Find linear regression and predicted line	
		y_pred1 = plot_lines(x1,y1, dy1)
		y_pred2 = plot_lines(x2,y2, dy2)
	
		## Finds min and max peaks
		min_pos = y1.argmin() 
		max_pos = y2.argmax()
	
		#plt.plot( x1[min_pos], y1[min_pos],'orange',marker='o', markersize=5)
		#plt.plot( x2[max_pos], y2[max_pos], 'orange',marker='o', markersize=5)
	
		max_pot = x2[max_pos]
		max_cur = y2[max_pos] - y_pred1[max_pos]
		min_pot = x1[min_pos]
		min_cur = y1[min_pos] - y_pred2[min_pos]
	
		plt.savefig(filename + '_saida.png')
		#plt.show()
		#out_data[] = {}
		out_data[filename] = {'Ipc': max_cur , 'Vpc': max_pot,'Ipa': min_cur, 'Vpa': min_pot}
		plt.clf()

	
	print '\nWriting to file...',
	myfile = open('output.txt', 'w')
	myfile.write('FileName\tIpc [ uA ]\tVpc [ V ]\tIpa [ uA ]\tVpa [ V ]\n')

	for name in out_data:
	    myString = "%s\t%.2f\t%.2f\t%.2f\t%.2f\n" % (name, out_data[name]['Ipc'], out_data[name]['Vpc'],out_data[name]['Ipa'], out_data[name]['Vpa'])
	    myfile.write(str(myString))
	     
	print 'Done!'

if __name__ == "__main__":
    main()
		 
