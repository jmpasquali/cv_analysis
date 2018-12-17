## FileName : cv_analysis.py
## Author: Joana Pasquali
## Calculate peak current from cyclic voltametry data
## Detect and remove value of capacitive current (background) from cyclic voltametry data 
## Date: november 5th 2018

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook


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
  
  	## Inclination coeff
        soma_x = soma(x)
        soma_x2 = multiplica(x,x) 
        soma_xy = multiplica(x,y) 
        media_x = media(x)
        media_y = media(y)
        m = (soma_xy - soma_x * media_y) / (soma_x2 - soma_x * media_x)
        
        ## Y axis intercept coeff
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

def finds_critical_idx(x, y): ## Finds index where data set is no longer linear 
	
	dy = np.diff(y)/(np.diff(x))
	
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
	
	## Uncomment to check whats going on 
	'''plt.plot(x[idx], ma20_num[idx], 'ro') ## Plot intersections 
	plt.plot(x[0:len(ma50)], ma50, x[0:len(ma20)], ma20) ## Plot moving averages'''

	return int(idx[0])

def calc_linear_background(x, y):

	idx = finds_critical_idx(x, y) + 25
	half_idx = int(0.5 * idx)
	m, b = find_coeffs(x[(idx - half_idx) : (idx + half_idx)], y[(idx - half_idx) : (idx + half_idx)])
	y_pred = y_predict(m, b, x)
	
	return y_pred

def graph_format(filename):

	warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
	plt.xlabel(' E [ V ]' )
	plt.ylabel(' I [ uA ] ')
	plt.title(filename[:-4])
	plt.grid(color='0', linewidth=0.1)
	ax = plt.subplot(111)    
	ax.spines["top"].set_visible(False)   
#	ax.spines["bottom"].set_visible(False)    
	ax.spines["right"].set_visible(False) 
#	ax.spines["left"].set_visible(False) 
#	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")   
	plt.xticks(fontsize=8)  
	plt.yticks(fontsize=8)
	    	
	    
def split_vector(vector):

	half = int(len(vector)/2)
	end = int(len(vector))
	vector_copy = np.array(vector)
	vector1 = vector_copy[0:half]
	vector2 = vector_copy[(half+1):end]
	
	return vector1, vector2

def main():
	
	validFileName = 0
	while(validFileName != 1):
		try:
			input =  raw_input('Name of txt containing file names list: ')
			# Import the files names from the input file 
			inputList = []
			with open(input,'rb') as csvfile:
			    spamreader = csv.reader(csvfile, delimiter=',', quotechar = '|')
			    for row in spamreader:
				name = str(row[0])
				inputList.append(name)
			validFileName = 1
		except:
			print 'Invalid input file ' + input 
	
	x_label = raw_input('X data column label: ')
	y_label =  raw_input('Y data column label: ')
	
	## Import file to pandas dataFrame
	out_data ={}
	validLabels = 0
	atLeastOne = 0
	
	for filename in inputList:

		validFileName = 1
		## Might have to change the separator and decimal for your data 
		try:
			data = pd.read_csv(filename, sep='\t',decimal=",")
		except: 
			print '\nInvalid file ' + filename + '!!!',
			validFileName = 0
			
		if (validFileName == 1):
		
			try:
				x = pd.to_numeric(data[x_label]) 
				y = pd.to_numeric(data[y_label])
				#x = pd.to_numeric(data['E /V']) 
				#y = pd.to_numeric(data['I /uA.1'])
			
				## Split vectors
				x1, x2 = split_vector(x)
				y1, y2 = split_vector(y)
	
				## Finds linear background 	
				y_pred1 = calc_linear_background(x1,y1)
				y_pred2 = calc_linear_background(x2,y2)
			
				## Cathodic peak current and potential 
				max_pos = y2.argmax()
				max_pot = x2[max_pos]
				max_cur = y2[max_pos] - y_pred2[max_pos]

				## Anodic peak current and potential 
				min_pos = y1.argmin() 
				min_pot = x1[min_pos]
				min_cur = y1[min_pos] - y_pred1[min_pos]
				out_data[filename] = {'Ipc': max_cur , 'Vpc': max_pot,'Ipa': min_cur, 'Vpa': min_pot}
				## Uncomment to check peaks position
				'''plt.plot( x1[min_pos], y1[min_pos],'orange',marker='o', markersize=5)
				plt.plot( x2[max_pos], y2[max_pos], 'orange',marker='o', markersize=5)'''
				
				## Plot all data 
				plt.plot(x1, y1, 'dodgerblue',linewidth=1) ##darkgrey
				plt.plot(x2, y2, 'dodgerblue', linewidth=1) ##dodgerblue  
				plt.plot(x1, y_pred1, color = "orangered", linestyle=':',linewidth=2) 
				plt.plot(x2, y_pred2, color = "orangered", linestyle=':',linewidth=2) 
				
				graph_format(filename)
				plt.savefig(filename + '_output_C.png')
				print '\nCreating plot for ' + filename + '...',
				plt.show()
				plt.clf()
				atLeastOne = 1
				
			except:
				print '\nData set ' + filename + ' could not be processed',
	
	if(atLeastOne == 1):
	
		## Writes to file
		print '\nWriting data to file...',
		myfile = open('output.txt', 'w')
		myfile.write('FileName\tIpc [ uA ]\tVpc [ V ]\tIpa [ uA ]\tVpa [ V ]\n')

		for name in out_data:
		    myString = "%s\t%.4f\t%.4f\t%.4f\t%.4f\n" % (name, out_data[name]['Ipc'], out_data[name]['Vpc'],out_data[name]['Ipa'], out_data[name]['Vpa'])
		    myfile.write(str(myString))
	
		print '\n\nDone!'
	else:
		print'\n\nMake sure column labels are correctly typed!!'

if __name__ == "__main__":
    main()
		 
